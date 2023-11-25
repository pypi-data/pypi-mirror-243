import setuptools

PACKAGE_NAME = "database-mysql-local"
package_dir = "circles_local_database_python"

with open('README.md') as f:
    readme = f.read()

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.123',  # https://pypi.org/project/database-mysql-local
    author="Circles",
    author_email="info@circles.life",
    url="https://github.com/circles-zone/database-mysql-local-python-package",
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
    # TOto avoid "pip install mysqlclient"
    install_requires=[
        "mysql-connector>=2.2.9",  # https://pypi.org/project/mysql-connector/
        "python-dotenv>=1.0.0",  # https://pypi.org/project/python-dotenv/
        "logger-local>=0.0.71",  # https://pypi.org/project/logger-local/
        "pytest>=7.4.3",  # https://pypi.org/project/pytest/
        "PyMySQL>=1.1.0",  # https://pypi.org/project/pymysql/
        # https://pypi.org/project/database-infrastructure-local/
        "database-infrastructure-local>=0.0.19"
    ]
)
