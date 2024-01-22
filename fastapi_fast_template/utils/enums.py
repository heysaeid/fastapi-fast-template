from enum import StrEnum


class EnumMixin:
    @classmethod
    def get_names(cls):
        result = []
        for item in cls:
            result.append(item.name)
        return list(result)

    @classmethod
    def get_values(cls):
        result = []
        for item in cls:
            result.append(item.value)
        return list(result)


class ConfigTypeEnum(EnumMixin, StrEnum):
    MULTIPLE = "multiple"
    SINGLE = "simple"


class DatabaseTypeEnum(EnumMixin, StrEnum):
    SQLALCHEMY = "sqlalchemy"
    TORTOISE = "tortoise"
    MONGODB = "mongodb"


class ArgumentDefaultValueEnum(StrEnum):
    APP_NAME = "Fast Template"
    CONFIG_TYPE = ConfigTypeEnum.MULTIPLE
    DATABASE_TYPE = DatabaseTypeEnum.SQLALCHEMY


class DirectoryEnum(StrEnum):
    logs = "./logs"
    tests = "./tests"
    src = "./src"
    src_routers = "./src/routers"
    src_repositories = "./src/repositories"
    src_services = "./src/services"
    src_models = "./src/models"
    src_schemas = "./src/schemas"
    src_utils = "./src/utils"
    src_tasks = "./src/tasks"


class FileEnum(StrEnum):
    fast_template_init = ".fast_template.ini"
    gitignore = ".gitignore"
    env_sample = ".env.sample"
    env = ".env"
    pre_commit_config = ".pre-commit-config.yaml"
    ruff_toml = "ruff.toml"

    tests_conftest = "tests/conftest.py"

    src_config = "src/config.py"
    src_app = "src/app.py"
    src_main = "src/main.py"
    src_database = "src/database.py"
    src_repo_base = "src/repositories/base.py"
    src_routers_init_ = "src/routers/__init__.py"
    src_utils_lifespan = "src/utils/lifespan.py"
    src_utils_caching = "src/utils/caching.py"
    src_tasks_init_ = "src/tasks/__init__.py"

    last_run_scheduler = ".last_run_scheduler.txt"


class ActionEnum(StrEnum):
    init = "init"
    extension = "extension"


class ExtensionNameEnum(StrEnum):
    babel = "babel"
    scheduler = "scheduler"
    caching = "caching"
