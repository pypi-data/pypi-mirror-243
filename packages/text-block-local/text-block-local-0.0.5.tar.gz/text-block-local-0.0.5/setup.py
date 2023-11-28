import setuptools

PACKAGE_NAME = "text-block-local"

package_dir = PACKAGE_NAME.replace("-", "_")

with open('README.md') as f:
    readme = f.read()

setuptools.setup(
    name=PACKAGE_NAME,  # https://pypi.org/project/text-block-local
    version='0.0.5',
    author="Circles",
    author_email="info@circles.life",
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pytest>=7.4.1',
        'database-infrastructure-local>=0.0.19',
        'logger-local>=0.0.71',
        'database-mysql-local>=0.0.116',
        'user-context-remote>=0.0.35'
    ]

)
