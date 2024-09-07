import os
from argparse import ArgumentParser
from pathlib import Path

from fastapi_fast_template.utils.enums import (
    ConfigTypeEnum,
    DependencyEnum,
    LoggingTypeEnum,
    ODMEnum,
    ORMEnum,
    StreamBrokerEnum,
)
from fastapi_fast_template.utils.helpers import get_app_config


class BaseContent:
    def __init__(self, args: ArgumentParser):
        self.app_config = get_app_config()

        if self.app_config:
            self.config_type = self.app_config["config_type"]
            self.orm_odm = self.app_config["orm_odm"]
            self.scheduler = (
                self.app_config.get("scheduler", "False") == "True"
            )
            self.caching = self.app_config.get("caching", "redis")
            self.stream = self.app_config.get("stream", "redis")
        else:
            self.config_type = args.config_type
            self.orm_odm = args.orm_odm
            self.stream = "redis"
            self.scheduler = False
            self.caching = "redis"

    def get_file_content(self, file_path: str, **kwargs) -> str:
        file = Path(f"{os.path.dirname(__file__)}/contents/{file_path}")
        file_content = file.read_text()

        content_data = {}
        for key, value in kwargs.items():
            if value is None:
                file_content = file_content.replace("{" + key + "}\n", "")
            else:
                content_data[key] = value

        if content_data:
            return file_content.format(**content_data)

        return file_content

    def install_dependencies(self, name: str):
        dependencies = {
            DependencyEnum.SQLALCHEMY: "pip install sqlalchemy[asyncio]",
            DependencyEnum.TORTOISE: "pip install tortoise-orm[asyncpg]",
            DependencyEnum.SQLMODEL: "pip install sqlmodel",
            DependencyEnum.BEANIE: "pip install beanie",
        }
        os.system(dependencies.get(name, ""))


class RootContent(BaseContent):
    def get_fast_template_ini(self) -> str:
        return f"""[app]
config_type={self.config_type}
orm_odm={self.orm_odm}"""

    def get_gitignore(self) -> str:
        return self.get_file_content(
            "git/.gitignore",
        )

    def get_env_sample(self) -> str:
        return self.get_file_content(
            "envs/.env.sample",
            db_env=self.get_db_env_sample(self.orm_odm),
        )

    def get_db_env_sample(self, orm_odm: ORMEnum | ODMEnum) -> str:
        config = {
            ORMEnum.SQLALCHEMY: "\nSQLALCHEMY_DB_URL=",
            ORMEnum.TORTOISE: "\nTORTOISE_DB_URL=",
            ORMEnum.SQLMODEL: "\nSQLMODEL_DB_URL=",
            ODMEnum.BEANIE: "\nBEANIE_DB_URL=",
        }
        return config[orm_odm]

    def get_conftest(self) -> str:
        return self.get_file_content("tests/conftest.py")

    def get_pre_commit(self) -> str:
        return self.get_file_content("git/.pre-commit-config.yaml")

    def get_ruff_toml(self) -> str:
        return self.get_file_content("ruff.toml")


class SrcContent(BaseContent):
    def get_config(self, app_name: str) -> str:
        config_types = {
            ConfigTypeEnum.MULTIPLE: "configs/config.py",
            ConfigTypeEnum.SINGLE: "configs/single_config.py",
        }
        return self.get_file_content(
            config_types[self.config_type],
            app_name=app_name,
            db_config=self.get_db_config(self.orm_odm),
        )

    def get_db_config(self, orm_odm: ORMEnum | ODMEnum) -> str:
        config = {
            ORMEnum.SQLALCHEMY: 'sqlalchemy_db_url: str = "postgresql+asyncpg://postgres:1234@localhost:5432/testdb"',
            ORMEnum.TORTOISE: 'tortoise_db_url: str = "postgres://postgres:1234@localhost:5432/testdb"',
            ORMEnum.SQLMODEL: 'sqlmodel_db_url: str = "postgres://postgres:1234@localhost:5432/testdb"',
            ODMEnum.BEANIE: 'mongo_connection: MongoDsn = "mongodb://localhost:27017/fast"',
        }
        return config[orm_odm]

    def get_app(self) -> str:
        return self.get_file_content(
            "main/app.py",
        )

    def get_main(self) -> str:
        return self.get_file_content(
            "main/main.py",
        )

    def get_database(self) -> str:
        config_types = {
            ORMEnum.SQLALCHEMY: "orm/sqlalchemy.py",
            ORMEnum.TORTOISE: "orm/tortoise.py",
            ORMEnum.SQLMODEL: "orm/sqlmodel.py",
            ODMEnum.BEANIE: "odm/beanie.py",
        }
        self.install_dependencies(self.orm_odm)
        return self.get_file_content(config_types[self.orm_odm])

    def get_repository(self) -> str:
        repository = {
            ORMEnum.SQLALCHEMY: "repositories/sqlalchemy/base.py",
            ORMEnum.TORTOISE: "repositories/tortoise/base.py",
            ORMEnum.SQLMODEL: "repositories/sqlmodel/base.py",
            ODMEnum.BEANIE: "repositories/beanie/base.py",
        }
        return self.get_file_content(
            repository[self.orm_odm],
        )

    def get_lifespan(self) -> str:
        start_application_content = "..."
        down_application_content = "..."
        import_content = ""

        if self.orm_odm == ORMEnum.TORTOISE:
            start_application_content = "await init_db()"
            down_application_content = "await close_db()"
            import_content += "from database import init_db, close_db"
        elif self.orm_odm == ORMEnum.SQLMODEL:
            start_application_content = "create_db_and_tables()"
            import_content += "from database import create_db_and_tables"

        return self.get_file_content(
            "utils/lifespan.py",
            start_application_content=start_application_content,
            down_application_content=down_application_content,
            import_content=import_content,
        )

    def get_router_init(self) -> str:
        return self.get_file_content("routers/base.py")


class ExtensionContent(BaseContent):
    def get_babel_cfg(self) -> str:
        return "[python: **.py]"

    def get_babel_import_in_app(self) -> str:
        return "from fastapi_and_babel import FastAPIAndBabel"

    def get_babel_in_app(self, lang: str) -> str:
        return f"""
    translator = FastAPIAndBabel(__file__, app, "{lang}")"""

    def get_babel_in_fast_template_init(self) -> str:
        return "\nbabel=True"

    def get_scheduler_in_fast_template_init(self) -> str:
        return "\nscheduler=True"

    def get_scheduler_init(self):
        return self.get_file_content("tasks/__init__.py")

    def get_scheduler_in_setting(self):
        return "\nenable_scheduler: bool = False"

    def get_scheduler_in_lifespan_import(self):
        return "from tasks import start_scheduler, shutdown_scheduler"

    def get_scheduler_in_lifespan_start_application(self):
        return "start_scheduler()"

    def get_scheduler_in_lifespan_down_application(self):
        return "shutdown_scheduler()"

    def get_caching_in_fast_template_init(self) -> str:
        return f"\ncaching={self.caching}"

    def get_caching_in_caching(self):
        if self.caching == "redis":
            return self.get_file_content("utils/caching/redis_cache.py")

    def get_caching_in_setting(self):
        return "\nredis_cache_namespace: str = 'ch'"

    def get_caching_in_lifespan_import(self):
        return "from .caching import cache"

    def get_caching_in_lifespan_start_application(self):
        return "await cache.init(settings.redis_url)"

    def get_caching_in_lifespan_down_application(self):
        return "await cache.close()"

    def get_logging_in_fast_template_init(self, type: LoggingTypeEnum) -> str:
        logging_type = {
            LoggingTypeEnum.INCOMING: "incoming_log=True",
            LoggingTypeEnum.APICALL: "apicall_log=True",
            LoggingTypeEnum.EXCEPTION: "exception_log=True",
        }
        return logging_type[type]

    def get_logging_import_in_app(self, type: LoggingTypeEnum) -> str:
        logging_type = {
            LoggingTypeEnum.INCOMING: "from fastapi_and_logging import FastAPIIncomingLog",
            LoggingTypeEnum.APICALL: "from fastapi_and_logging import ExceptionLogger",
            LoggingTypeEnum.EXCEPTION: "from fastapi_and_logging.http_clients import HTTPXLogger",
        }
        return logging_type[type]

    def get_logging_class_in_app(self, type: LoggingTypeEnum) -> str:
        logging_type = {
            LoggingTypeEnum.INCOMING: "\tFastAPIIncomingLog(app)",
            LoggingTypeEnum.APICALL: "\texception_logger = ExceptionLogger(app=app)",
            LoggingTypeEnum.EXCEPTION: "\tHTTPXLogger()",
        }
        return logging_type[type]

    def get_stream_in_fast_template_init(self) -> str:
        return f"\nstream={self.stream}"

    def get_stream_in_config(self) -> str:
        stream_brokers = {
            StreamBrokerEnum.AIOKAFKA: '\nbroker_url: str = "localhost:9092"',
            StreamBrokerEnum.CONFLUENT: '\nbroker_url: str = "localhost:9092"',
            StreamBrokerEnum.RABBIT: '\nbroker_url: str = "amqp://guest:guest@localhost:5672/"',
            StreamBrokerEnum.REDIS: '\nbroker_url: str = "redis://localhost:6379"',
            StreamBrokerEnum.NATS: '\nbroker_url: str = "nats://localhost:4222"',
        }
        return stream_brokers[self.stream]

    def get_stream_in_stream(self) -> str:
        stream_brokers = {
            StreamBrokerEnum.AIOKAFKA: {
                "import_faststream_broker": "from faststream.kafka import KafkaBroker",
                "faststream_broker": "KafkaBroker",
            },
            StreamBrokerEnum.CONFLUENT: {
                "import_faststream_broker": "from faststream.confluent import KafkaBroker",
                "faststream_broker": "KafkaBroker",
            },
            StreamBrokerEnum.RABBIT: {
                "import_faststream_broker": "from faststream.rabbit import RabbitBroker",
                "faststream_broker": "RabbitBroker",
            },
            StreamBrokerEnum.REDIS: {
                "import_faststream_broker": "from faststream.redis import RedisBroker",
                "faststream_broker": "RedisBroker",
            },
            StreamBrokerEnum.NATS: {
                "import_faststream_broker": "from faststream.nats import NatsBroker",
                "faststream_broker": "NatsBroker",
            },
        }
        return (self.get_file_content("main/stream.py")).format(
            **stream_brokers[self.stream]
        )

    def get_stream_in_lifespan(self) -> str:
        return "\n\n" + self.get_file_content("utils/stream_lifespan.py")

    def get_authx_in_fast_template_init(self) -> str:
        return "auth=True"

    def get_authx(self) -> str:
        return self.get_file_content("utils/authx.py")

    def get_authx_in_app(self) -> str:
        return "from utils.auth import auth"

    def get_authx_import_in_app(self) -> str:
        return "auth.handle_errors(app)"
