from config import settings
from fastapi import FastAPI

from routers import api_router
from utils.lifespan import lifespan


def create_app() -> FastAPI:
    app = FastAPI(
        debug=settings.debug,
        title=settings.app_name,
        description=settings.description,
        lifespan=lifespan,
    )
    app.include_router(api_router)
    return app
