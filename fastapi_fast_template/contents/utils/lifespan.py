from contextlib import asynccontextmanager

from fastapi import FastAPI

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
