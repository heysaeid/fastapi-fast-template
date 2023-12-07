from typing import AsyncGenerator
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings


url = URL.create(
    drivername = settings.db_drivername,
    username = settings.db_username,
    password = settings.db_password,
    host = settings.db_host,
    database = settings.db_database,
    port = settings.db_port,
)

engine = create_async_engine(url)
Base = declarative_base()
async_session = sessionmaker(
    autocommit = False, 
    autoflush = False,
    expire_on_commit = False, 
    bind = engine, 
    class_ = AsyncSession
)

async def create_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        
async def drop_and_create_all_tables():
    await drop_all_tables()
    await create_all_tables()

async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session