import json
import re
import time
from datetime import datetime

import mysql.connector
from circles_local_database_python.generic_crud import GenericCRUD
from circles_number_generator.number_generator import NumberGenerator
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from user_context_remote.user_context import UserContext

MAX_ERRORS = 5
TEXT_BLOCK_COMPONENT_ID = 143
TEXT_BLOCK_COMPONENT_NAME = "text_block_local_python_package"
DEVELOPER_EMAIL = "akiva.s@circ.zone"
object1 = {
    'component_id': TEXT_BLOCK_COMPONENT_ID,
    'component_name': TEXT_BLOCK_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}
logger = Logger.create_logger(object=object1)


class TextBlocks(GenericCRUD):
    def __init__(self):
        super().__init__(default_schema_name="text_block")
        UserContext.login_using_user_identification_and_password()
        self.errors_count = 0

    def get_block_fields(self, text_block_type_id: int) -> dict:
        """Retrieves regular expressions and field IDs based on the provided `block_type_id`."""
        logger.start("Getting regex and field_id from block_id ...")
        self.set_schema(schema_name="field")
        # One field id can have multiple regexes
        block_fields = dict(self.select_multi_tuple_by_where(view_table_name="block_type_field_view",
                                                             select_clause_value="regex, field_id",
                                                             where="block_type_id = %s OR block_type_id IS NULL",
                                                             params=(text_block_type_id,)))

        logger.end("Regex and field ids retrieved", object={'block_fields': block_fields})
        return block_fields

    def get_fields(self) -> dict:
        """Retrieves field IDs and names from the database."""
        logger.start("Getting field ids and names ...")
        self.set_schema(schema_name="field")
        fields = dict(self.select_multi_tuple_by_where(view_table_name="field_view",
                                                       select_clause_value="field_id, name"))

        logger.end("Field names and ids retrieved", object={'fields': fields})
        return fields

    def get_block_type_ids_regex(self) -> dict:
        """Retrieves block type IDs and regular expressions from the database."""
        # TODO: we also have regexes in block_type_field_table, should we return those as well?
        logger.start("Getting block type ids and names ...")
        self.set_schema(schema_name="text_block_type")
        # One regex can have multiple block type ids
        block_types = dict(self.select_multi_tuple_by_where(view_table_name="text_block_type_regex_view",
                                                            select_clause_value="regex, text_block_type_id"))

        logger.end("Block types retrieved", object={'block_types': block_types})
        return block_types

    def get_block_types(self) -> dict:
        """Retrieves block type IDs and names from the database."""
        logger.start("Getting block type ids and names ...")
        self.set_schema(schema_name="text_block_type")
        block_types = dict(self.select_multi_tuple_by_where(view_table_name="text_block_type_ml_view",
                                                            select_clause_value="text_block_type_id, name"))

        logger.end("Block types retrieved", object={'block_types': block_types})
        return block_types

    def get_text_block_ids_types(self) -> dict:
        """Retrieves text block IDs and types from the database."""
        logger.start("Getting text blocks from text_block_table ...")
        self.set_schema(schema_name="text_block")
        result = self.select_multi_tuple_by_where(view_table_name="text_block_view",
                                                  select_clause_value="text_block_type_id, text_block_type_id, text_without_empty_lines, text")
        text_block_ids_types = {}
        for text_block_id, type_id, text_without_empty_lines, text in result:
            text_block_ids_types[text_block_id] = (type_id, text_without_empty_lines or text)

        logger.end("Text blocks retrieved", object={'text_blocks_ids_types': text_block_ids_types})
        return text_block_ids_types

    def process_text_blocks_updated_since_date(self, since_date: datetime) -> None:
        self.set_schema(schema_name="text_block")
        text_block_ids = self.select_multi_tuple_by_where(view_table_name="text_block_view",
                                                          select_clause_value="text_block_type_id",
                                                          where="updated_timestamp >= %s",
                                                          params=(since_date,))
        for text_block_id in text_block_ids:
            self.process_text_block_by_id(text_block_id[0])

    def process_text_block_by_id(self, text_block_id: int) -> None:
        """
        1. Retrieves the text and other details of the text block.
        2. Reformat the text if needed.
        3. Identifies and updates the text block type.
        4. Extract fields from the text based on the block type's regular expressions.
        5. Updates the text block with the extracted fields in JSON format.
        """

        try:
            text, text_block_type_id, profile_id = self.get_text_block_details(text_block_id)

            # reformat text
            text = text.replace("\n", " ")

            if text_block_type_id is None:
                text_block_type_id = self.identify_and_update_text_block_type(text_block_id, text)

            fields_dict = self.extract_fields_from_text(text, text_block_type_id, profile_id)
            self.update_text_block_fields(text_block_id, fields_dict)

        except mysql.connector.errors.DatabaseError as e:
            if "Lock wait timeout exceeded" in str(e) and self.errors_count < MAX_ERRORS:  # prevent infinite loop
                self.errors_count += 1
                logger.warn("Lock wait timeout exceeded. Retrying UPDATE after a short delay.")
                time.sleep(2)
                self.process_text_block_by_id(text_block_id)
            else:
                logger.exception("Database Error", object=e)

        except Exception as e:
            logger.exception("Error processing text block", object=e)

        self.errors_count = 0

    def get_text_block_details(self, text_block_id: int) -> tuple:
        """Retrieves text and related details for a given text block ID."""
        logger.start("Getting text block details ...", object={'text_block_type_id': text_block_id})
        self.set_schema(schema_name="text_block")
        result = self.select_one_tuple_by_id(view_table_name="text_block_view",
                                             select_clause_value="text_without_empty_lines, text, text_block_type_id, profile_id",
                                             id_column_name="text_block_id",
                                             id_column_value=text_block_id)

        if result[0]:
            text, text_block_type_id, profile_id = (result[0], result[2], result[3])
        else:
            text, text_block_type_id, profile_id = (result[1], result[2], result[3])

        return text, text_block_type_id, profile_id

    def extract_fields_from_text(self, text: str, text_block_type_id: int, profile_id: int) -> dict:
        """Extracts fields from the text based on the block type's regular expressions."""
        fields_dict = {}
        block_fields = self.get_block_fields(text_block_type_id)
        fields = self.get_fields()

        for regex, field_id in block_fields.items():
            if not regex:  # we have not defined those yet in the block_type_field_table
                continue
            try:
                re.compile(regex)
                matches = re.findall(regex, text)

                if not matches:
                    continue
                field = fields[field_id]
                fields_dict[field] = matches

                for match in matches:
                    self.process_and_update_field(profile_id, fields_dict, field_id, match)

            except re.error as e:
                logger.exception(f"Invalid regex: {regex}", object=e)

        return fields_dict

    def process_and_update_field(self, profile_id: int, fields_dict: dict, field_id: int, match: str) -> None:
        """Processes and updates the field."""
        # TODO: rewrite this method
        # https://github.com/circles-zone/text-block-local-python-package/blob/613e6cdbf5c5f54b40c37e4b479e0d48d820a03b/circles_text_block_local/text_block_microservice.py#L181
        logger.start("Processing and updating field ...", object={
            'profile_id': profile_id, 'field_id': field_id, 'match': match})
        self.set_schema(schema_name="field")
        field_info = self.select_one_tuple_by_id(
            view_table_name='field_view',
            select_clause_value="table_id, database_field_name, database_sub_field_name, database_sub_field_value, processing_id, processing_database_field_name",
            id_column_value=field_id)
        table_id, database_field_name, database_sub_field_name, database_sub_field_value, processing_id, processing_database_field_name = field_info

        try:
            # TODO: process fields with _original
            # processed_value = self.process_field(processing_id, match)

            # Retrieve table definition
            self.set_schema(schema_name="database")

            # get table definition
            schema, table_name, profile_mapping_table_id = self.select_one_tuple_by_id(
                view_table_name='table_definition_view',
                select_clause_value="schema, table_name, profile_mapping_table_id",
                id_column_name="id", id_column_value=table_id)

            # Get field information
            profile_mapping_table_schema, profile_mapping_table_name = self.select_one_tuple_by_id(
                view_table_name='table_definition_view', select_clause_value="`schema`, table_name",
                id_column_name="id", id_column_value=profile_mapping_table_id)

            if profile_id and profile_mapping_table_id:
                # Set the correct schema for profile mapping
                self.set_schema(schema_name=schema)

                # Retrieve mapping ID for the profile
                select_clause_value = schema + "_id"
                mapping_id = self.select_one_dict_by_id(view_table_name=table_name,
                                                        select_clause_value=select_clause_value,
                                                        id_column_name="profile_id",
                                                        id_column_value=profile_id)[select_clause_value]
                sql = "SELECT %s FROM %s.%s WHERE id = %s" % (database_field_name, schema, table_name, mapping_id)
                self.cursor.execute(sql)
                field_old = self.cursor.fetchone()
                if field_old is not None:
                    sql = "UPDATE %s.%s SET %s = '%s' WHERE id = %s" % (
                        schema, table_name, database_field_name, match, mapping_id)
                    if database_sub_field_name and database_sub_field_value:
                        sql = "UPDATE %s.%s SET %s = '%s', %s = '%s' WHERE id = %s" % (
                            schema, table_name, database_field_name, match, database_sub_field_name,
                            database_sub_field_value, mapping_id)
                    self.cursor.execute(sql)
                    self.connection.commit()
                    if field_old[0] != match:
                        self.update_logger_with_old_and_new_field_value(field_id, field_old[0], match)

            else:
                created_user_id = updated_user_id = UserContext().get_effective_user_id()
                # Populate the person/profile class for each profile processed
                profile_id = self.create_person_profile(fields_dict)

                # insert information from extracted fields
                sql = "INSERT IGNORE INTO %s.%s (%s, created_user_id, updated_user_id) VALUES ('%s', %s, %s)" % (
                    schema, table_name, database_field_name, match, created_user_id, updated_user_id)
                if database_sub_field_name and database_sub_field_value:
                    sql = "INSERT IGNORE INTO %s.%s (%s, %s, created_user_id, updated_user_id) VALUES ('%s', '%s', %s, %s)" % (
                        schema, table_name, database_field_name, database_sub_field_name, match,
                        database_sub_field_value,
                        created_user_id, updated_user_id)
                logger.info(object={"SQL command executed": sql})
                self.cursor.execute(sql)
                mapping_id = self.cursor.lastrowid
                self.connection.commit()

                # update the profile_mapping table
                if profile_mapping_table_schema:
                    sql = "INSERT IGNORE INTO %s.%s (profile_id, %s_id, created_user_id, updated_user_id) VALUES (%s, %s, %s, %s)" % (
                        profile_mapping_table_schema, profile_mapping_table_name, schema, profile_id, mapping_id,
                        created_user_id, updated_user_id)
                    if profile_mapping_table_schema == "group_profile":
                        sql = "INSERT IGNORE INTO %s.%s (profile_id, %s_id, relationship_type_id, created_user_id, updated_user_id) VALUES (%s, %s, %s, %s, %s)" % (
                            profile_mapping_table_schema, profile_mapping_table_name, schema, profile_id, 5, mapping_id,
                            created_user_id, updated_user_id)
                    self.cursor.execute(sql)
                    self.connection.commit()

        except Exception as e:
            logger.exception("Error processing field", object=e)

    def update_text_block_fields(self, text_block_id: int, fields_dict: dict) -> None:
        """Updates the text block with the extracted fields in JSON format."""
        logger.start("Updating text block fields ...", object={'text_block_id': text_block_id})
        fields_json = json.dumps(fields_dict)
        self.set_schema(schema_name="text_block")
        self.update_by_id(table_name="text_block_table", id_column_name="text_block_id", id_column_value=text_block_id,
                          data_json={"fields_extracted_json": fields_json})

    def identify_and_update_text_block_type(self, text_block_id: int, text: str) -> int:
        """Identifies and updates the text block type."""
        logger.start("Identifying and updating block type for text block", object={
            'text_block_id': text_block_id, 'text': text})
        text_block_type_id = self.identify_text_block_type(text, text_block_id)
        if text_block_type_id is not None:
            self.set_schema(schema_name="text_block")
            self.update_by_id(table_name="text_block_table", id_column_name="text_block_id",
                              id_column_value=text_block_id,
                              data_json={"text_block_type_id": text_block_type_id})

        return text_block_type_id

    def identify_text_block_type(self, text: str, text_block_id: int = None) -> int:
        """Identifies the text block type.
        If a text block ID is provided, it will first try to identify the block type based on its system ID and entity ID."""
        logger.start("Identifying block type for text block", object={'text_block_id': text_block_id, 'text': text})
        self.set_schema(schema_name="text_block_type")
        results = None
        if text_block_id:
            system = self.select_one_dict_by_id(view_table_name="text_block_type_view",
                                                select_clause_value="system_id, system_entity_id",
                                                id_column_name="text_block_type_id",
                                                id_column_value=text_block_id)
            # filter results with system_id and system_entity if possible
            if "system_entity_id" in system:
                results = self.select_multi_tuple_by_where(view_table_name="text_block_type_view",
                                                           select_clause_value="regex",
                                                           where="system_id = %s AND system_entity_id = %s",
                                                           params=(system["system_id"], system["system_entity_id"]))

            elif "system_id" in system:
                results = self.select_multi_tuple_by_id(view_table_name="text_block_type_view",
                                                        select_clause_value="regex",
                                                        id_column_name="system_id",
                                                        id_column_value=system["system_id"])
        if results and any(x[0] for x in results):
            regex_list = "(" + ",".join(str(regex[0]) for regex in results if regex[0]) + ")"
            potential_block_type_ids = dict(self.select_multi_tuple_by_where(
                view_table_name="text_block_type_regex_view",
                select_clause_value="text_block_type_id, regex",
                where="regex IN %s",
                params=(regex_list,)))
        else:
            logger.info("No system id for text block")
            potential_block_type_ids = self.get_block_type_ids_regex()

        # classify block_type using regex
        for regex, text_block_type_id in potential_block_type_ids.items():
            try:
                re.compile(regex)
                match = re.search(regex, text)
                if match:
                    return text_block_type_id
            except (re.error, TypeError) as e:
                logger.exception(f"Invalid regex: {regex}", object=e)

        # if no block type id has been found by this point
        logger.end("Unable to identify block_type_id for text block", object={'text_block_id': text_block_id})

    def check_all_text_blocks(self) -> None:
        """Checks all text blocks and updates their block type if needed."""
        # For all text_blocks
        logger.start("Checking all text blocks ...")
        text_block_ids_types = self.get_text_block_ids_types()
        block_types = self.get_block_types()
        for block_type_id in text_block_ids_types:
            existing_block_type = text_block_ids_types[block_type_id][0]
            if existing_block_type:
                logger.info("\nOld block type: " + str(existing_block_type) + ", '" + block_types[
                    existing_block_type] + "' for text block " + str(block_type_id))
            else:
                logger.info("Old block type: None")
            text = (text_block_ids_types[block_type_id][1]).replace("\n", " ")
            new_block_type = self.identify_and_update_text_block_type(block_type_id, text)
            if new_block_type is not None:
                logger.info("Identified block type: " + str(new_block_type) + " " + block_types[new_block_type])
        logger.end("All text blocks checked")

    def update_logger_with_old_and_new_field_value(self, field_id: int, field_value_old: str,
                                                   field_value_new: str) -> int:
        """Updates the logger with the old and new field value."""
        logger.start("Updating logger with old and new field value", object={
            'field_id': field_id, 'field_value_old': field_value_old, 'field_value_new': field_value_new})
        self.set_schema(schema_name="logger")
        data_json = {"field_id": field_id, "field_value_old": field_value_old, "field_value_new": field_value_new}
        logger_id = self.insert(table_name="logger_table", data_json=data_json)
        logger.end("Logger updated", object={'logger_id': logger_id})
        return logger_id

    def create_person_profile(self, fields_dict: dict) -> int:
        """Creates a person and profile based on the provided fields."""
        logger.start("Creating person and profile ...")
        self.set_schema(schema_name="person")
        created_user_id = UserContext().get_effective_user_id()
        number = NumberGenerator.get_random_number("person", "person_table")
        if "First Name" in fields_dict and "Last Name" in fields_dict:
            first_name = fields_dict["First Name"][0]
            last_name = fields_dict["Last Name"][0]
            data_json = {"number": number, "first_name": first_name, "last_name": last_name,
                         "last_coordinate": "POINT(0.0000, 0.0000)", "created_user_id": created_user_id}
        elif "Birthday" in fields_dict:
            birthday = fields_dict["Birthday"][0]
            data_json = {"number": number, "birthday_original": birthday, "last_coordinate": "POINT(0.0000, 0.0000)",
                         "created_user_id": created_user_id}
        else:
            data_json = {"number": number, "last_coordinate": "POINT(0.0000, 0.0000)",
                         "created_user_id": created_user_id}
        self.insert(table_name="person_table", data_json=data_json)

        person_id = self.cursor.lastrowid()
        visibility_id = 0  # TODO: replace this magic number.
        self.set_schema(schema_name="profile")
        data_json = {"number": number, "person_id": person_id, "visibility_id": visibility_id,
                     "created_user_id": created_user_id}
        self.insert(table_name="profile_table", data_json=data_json)

        profile_id = self.cursor.lastrowid()
        logger.end("Person and profile created", object={'person_id': person_id, 'profile_id': profile_id})

        return profile_id

    def process_field(self, processing_id, match):
        pass
        # if processing_id == 1: #birthday YYYY-MM-DD

        # else if processing_id ==2: #phone

        # return processed_value
