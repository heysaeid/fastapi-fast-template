from fastapi import FastAPI
from contextlib import asynccontextmanager

{import_content}


async def start_application() -> None:
    {start_application_content}


async def down_application() -> None:
    {down_application_content}


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_application()

    yield

    await down_application()
