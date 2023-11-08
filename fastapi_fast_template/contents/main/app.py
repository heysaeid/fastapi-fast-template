from fastapi import FastAPI
from config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        debug = settings.debug, 
        title = settings.app_name, 
        description = settings.description
    )
    return app