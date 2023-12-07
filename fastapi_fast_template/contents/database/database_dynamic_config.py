from fastapi_fast_template.utils.enums import DatabaseTypeEnum


class DatabaseDynamicConfig:
    DBMS_DATABASES = (DatabaseTypeEnum.SQLALCHEMY, DatabaseTypeEnum.TORTOISE)
    
    @classmethod
    def get_db_config(cls, database_type: DatabaseTypeEnum) -> str | None:
        DBMS_CONTENT = """
    # Database Configs
    db_drivername: str = "postgresql+asyncpg"
    db_username: str = "postgres"
    db_password: str = "1234"
    db_host: str = "localhost"
    db_database: str = "fastdb"
    db_port: int = 5432"""

        if database_type in cls.DBMS_DATABASES:
            return DBMS_CONTENT
    
    @classmethod
    def get_db_env_sample(cls, database_type: DatabaseTypeEnum) -> str | None:
        DBMS_CONTENT = """
# Database Configs
DB_DRIVERNAME=
DB_USERNAME=
DB_PASSWORD=
DB_HOST=
DB_DATABASE=
DB_PORT="""

        if database_type in cls.DBMS_DATABASES:
            return DBMS_CONTENT