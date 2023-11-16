from fastapi import FastAPI
from config import settings
from utils.lifespan import lifespan
from routers import api_router


def create_app() -> FastAPI:
    app = FastAPI(
        debug = settings.debug, 
        title = settings.app_name, 
        description = settings.description,
        lifespan=lifespan,
    )
    app.include_router(api_router)
    return app