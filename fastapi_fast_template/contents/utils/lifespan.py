from fastapi import FastAPI
from contextlib import asynccontextmanager


async def start_application() -> None:
    ...
    
async def down_application() -> None:
    ...

@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_application()
        
    yield
    
    await down_application()