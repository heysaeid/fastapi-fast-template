from contextlib import asynccontextmanager

from fastapi import FastAPI

{import_content}  # noqa: B018


async def start_application() -> None:
    {start_application_content}  # noqa: B018


async def down_application() -> None:
    {down_application_content}  # noqa: B018


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_application()

    yield

    await down_application()
