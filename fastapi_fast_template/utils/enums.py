from strenum import StrEnum


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


class ORMEnum(EnumMixin, StrEnum):
    SQLALCHEMY = "sqlalchemy"
    TORTOISE = "tortoise"
    SQLMODEL = "sqlmodel"


class DependencyEnum(EnumMixin, StrEnum):
    SQLALCHEMY = "sqlalchemy"
    TORTOISE = "tortoise"
    SQLMODEL = "sqlmodel"
    BEANIE = "beanie"


class ODMEnum(EnumMixin, StrEnum):
    BEANIE = "beanie"


class CachingBackendEnum(EnumMixin, StrEnum):
    REDIS = "redis"


class LoggingTypeEnum(EnumMixin, StrEnum):
    INCOMING = "incoming"
    APICALL = "apicall"
    EXCEPTION = "exception"


class StreamBrokerEnum(EnumMixin, StrEnum):
    REDIS = "redis"
    AIOKAFKA = "aiokafka"
    CONFLUENT = "confluent"
    RABBIT = "rabbit"
    NATS = "nats"


class AuthEnum(EnumMixin, StrEnum):
    AUTHX = "auth"


class ArgumentDefaultValueEnum(StrEnum):
    APP_NAME = "Fast Template"
    CONFIG_TYPE = ConfigTypeEnum.MULTIPLE
    ORM_ODM = ORMEnum.SQLALCHEMY
    REDIS_BACKEND = CachingBackendEnum.REDIS
    LOGGING_TYPE = LoggingTypeEnum.INCOMING
    STREAM_BROKER = StreamBrokerEnum.REDIS
    AUTH = AuthEnum.AUTHX


class DirectoryEnum(StrEnum):
    LOGS = "./logs"
    TESTS = "./tests"
    SRC = "./src"
    SRC_ROUTERS = "./src/routers"
    SRC_REPOSITORIES = "./src/repositories"
    SRC_SERVICES = "./src/services"
    SRC_MODELS = "./src/models"
    SRC_SCHEMAS = "./src/schemas"
    SRC_UTILS = "./src/utils"
    SRC_TASKS = "./src/tasks"


class FileEnum(StrEnum):
    FAST_TEMPLATE_INIT = ".fast_template.ini"
    GITIGNORE = ".gitignore"
    ENV_SAMPLE = ".env.sample"
    ENV = ".env"
    PRE_COMMIT_CONFIG = ".pre-commit-config.yaml"
    RUFF_TOML = "ruff.toml"

    TESTS_CONFTEST = "tests/conftest.py"

    SRC_CONFIG = "src/config.py"
    SRC_APP = "src/app.py"
    SRC_MAIN = "src/main.py"
    SRC_DATABASE = "src/database.py"
    SRC_STREAM = "src/stream.py"
    SRC_REPO_BASE = "src/repositories/base.py"
    SRC_ROUTERS_INIT_ = "src/routers/__init__.py"
    SRC_UTILS_LIFESPAN = "src/utils/lifespan.py"
    SRC_UTILS_CACHING = "src/utils/caching.py"
    SRC_UTILS_AUTHX = "src/utils/auth.py"
    SRC_TASKS_INIT_ = "src/tasks/__init__.py"

    LAST_RUN_SCHEDULER = ".last_run_scheduler.txt"


class ActionEnum(StrEnum):
    INIT = "init"
    EXTENSION = "extension"


class ExtensionNameEnum(StrEnum):
    BABEL = "babel"
    SCHEDULER = "scheduler"
    CACHING = "caching"
    LOGGING = "logging"
    STREAM = "stream"
    AUTH = "auth"
