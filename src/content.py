class BaseContent:
    
    def get_gitignore() -> str:
        return """.idea
.ipynb_checkpoints
.mypy_cache
.vscode
__pycache__
.pytest_cache
htmlcov
dist
site
.coverage
coverage.xml
.netlify
test.db
log.txt
Pipfile.lock
env3.*
env
.env
docs_build
venv
docs.zip
archive.zip

logs/*

# vim temporary files
*~
.*.sw?"""

    def get_config() -> str:
        return """from pydantic import BaseSettings


class Settings(BaseSettings):
    app_env: str = "dev"
    debug: bool = True
    project_name: str = "Logistic Core"
    description: str = ""
    
    class Config:
        env_file = ".env"

   
class DevSettings(Settings):
    pass


class TestSettings(Settings):
    pass


class ProdSettings(Settings):
    debug: bool = False


def get_settings():
    env = Settings().app_env
    
    if env == "dev":
        return DevSettings()
    elif env == "test":
        return TestSettings()
    elif env == "prod":
        return ProdSettings()
    else:
        raise ValueError("Invalid APP_ENV value")
    

settings = get_settings()"""

    def get_app() -> str:
        return """from fastapi import FastAPI
from config import settings


def create_app() -> FastAPI:
    app = FastAPI(debug=settings.debug, title=settings.project_name, description=settings.description)
    return app"""
    
    
    def get_main() -> str:
        return """import uvicorn
from app import create_app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, env_file=".env")"""