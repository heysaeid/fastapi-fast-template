import os
from argparse import ArgumentParser
from pathlib import Path

from fastapi_fast_template.utils.enums import ConfigTypeEnum, DatabaseTypeEnum
from fastapi_fast_template.utils.helpers import get_app_config


class BaseContent:
    def __init__(self, args: ArgumentParser):
        self.app_config = get_app_config()

        if self.app_config:
            self.config_type = self.app_config["config_type"]
            self.database_type = self.app_config["database_type"]
            self.scheduler = (
                self.app_config.get("scheduler", "False") == "True"
            )
            self.caching = self.app_config.get("caching", "redis")
        else:
            self.config_type = args.config_type
            self.database_type = args.database_type
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


class RootContent(BaseContent):
    def get_fast_template_ini(self) -> str:
        return f"""
[app]
config_type = {self.config_type}
database_type = {self.database_type}"""

    def get_gitignore(self) -> str:
        return self.get_file_content(
            "git/.gitignore",
        )

    def get_env_sample(self) -> str:
        return self.get_file_content(
            "envs/.env.sample",
            db_env=self.get_db_env_sample(self.database_type),
        )

    def get_db_env_sample(self, database: DatabaseTypeEnum) -> str:
        config = {
            DatabaseTypeEnum.SQLALCHEMY: "SQLALCHEMY_DB_URL=",
            DatabaseTypeEnum.TORTOISE: "TORTOISE_CONFIG_FILE=",
        }
        return config[database]

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
            db_config=self.get_db_config(self.database_type),
        )

    def get_db_config(self, database: DatabaseTypeEnum) -> str:
        config = {
            DatabaseTypeEnum.SQLALCHEMY: 'sqlalchemy_db_url: str = "postgresql+asyncpg://postgres:1234@localhost:5432/testdb"',
            DatabaseTypeEnum.TORTOISE: 'tortoise_db_url: str = "postgres://postgres:1234@localhost:5432/testdb"',
        }
        return config[database]

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
            DatabaseTypeEnum.SQLALCHEMY: "database/sqlalchemy.py",
            DatabaseTypeEnum.TORTOISE: "database/tortoise.py",
        }
        return self.get_file_content(
            config_types[self.database_type],
        )

    def get_repository(self) -> str:
        repository = {
            DatabaseTypeEnum.SQLALCHEMY: "repositories/sqlalchemy/base.py",
            DatabaseTypeEnum.TORTOISE: "repositories/tortoise/base.py",
        }
        return self.get_file_content(
            repository[self.database_type],
        )

    def get_lifespan(self) -> str:
        start_application_content = "..."
        down_application_content = "..."
        import_content = ""

        if self.database_type == DatabaseTypeEnum.TORTOISE:
            start_application_content = "await init_db()"
            down_application_content = "await close_db()"
            import_content += "from database import init_db, close_db"

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
