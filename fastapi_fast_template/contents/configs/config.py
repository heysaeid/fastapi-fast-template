from enum import Enum
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppEnvironmentEnum(str, Enum):
    DEVELOPMENT = "dev"
    PRODUCTION = "prod"
    TEST = "test"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    app_env: str = AppEnvironmentEnum.DEVELOPMENT
    app_name: str = "{app_name}"
    app_port: int = 8000
    debug: bool = True
    description: str = ""
    {db_config}  # noqa: B018


class DevSettings(Settings):
    pass


class TestSettings(Settings):
    pass


class ProdSettings(Settings):
    debug: bool = False


@lru_cache
def get_settings():
    env = Settings().app_env

    if env == AppEnvironmentEnum.DEVELOPMENT:
        return DevSettings()
    elif env == AppEnvironmentEnum.TEST:
        return TestSettings()
    elif env == AppEnvironmentEnum.PRODUCTION:
        return ProdSettings()

    raise ValueError("Invalid APP_ENV value")


settings = get_settings()
