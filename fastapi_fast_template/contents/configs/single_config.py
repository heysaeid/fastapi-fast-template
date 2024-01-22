from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    app_env: str = "dev"
    app_name: str = "Awesome API"
    app_port: int = 8000
    debug: bool = True
    description: str = ""
    {db_config}  # noqa: B018


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
