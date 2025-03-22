import os
from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import create_async_engine


def uri(dialect, driver):
    """
    https://github.com/libwww-perl/URI-db
    """
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASS")
    host = os.environ.get("DB_HOST")
    port = os.environ.get("DB_PORT")
    db_name = os.environ.get("DB_NAME")
    ###
    scheme = f"{dialect}+{driver}"
    user_info = f"{user}:{password}"
    authority = f"{user_info}@{host}:{port}"
    authority = "" if authority == ":@:" else authority
    return f"{scheme}://{authority}/{db_name}"


def create(dialect: str = "mysql", driver: str = None, asyncronous: bool = False):
    if not driver:
        match dialect:
            case "mysql" | "mariadb":
                """
                sync = "https://pypi.org/project/mysql-connector-python/"
                async = https://github.com/long2ice/asyncmy
                """
                driver = "mysqlconnector" if not asyncronous else "asyncmy"
            case "postgres":
                """
                https://pypi.org/project/psycopg/
                """
                driver = "psycopg" if not asyncronous else "psycopg_async"
            case "sqlite":
                """
                sync = default of selite3 builtin lib
                async = https://pypi.org/project/aiosqlite/
                """
                driver = "pysqlite" if not asyncronous else "aiosqlite"
            case "oracle":
                """
                https://oracle.github.io/python-oracledb/
                """
                driver = "oracledb" if not asyncronous else "oracledb"
            case "mssql":
                """
                sync = pymssql is a Python module that provides a Python DBAPI interface around FreeTDS.
                async = https://pypi.org/project/aioodbc/
                """
                driver = "pymssql" if not asyncronous else "aioodbc"
            case _:
                raise Exception(f"Unsupported dialect/DBAPI {dialect}")
    db_uri = uri(dialect, driver)
    return create_engine(db_uri) if not asyncronous else create_async_engine(db_uri)
