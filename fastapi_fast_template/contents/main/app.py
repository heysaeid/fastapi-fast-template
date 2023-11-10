from fastapi import FastAPI
from config import settings
from utils.lifespan import lifespan


def create_app() -> FastAPI:
    app = FastAPI(
        debug = settings.debug, 
        title = settings.app_name, 
        description = settings.description,
        lifespan=lifespan,
    )
    return app