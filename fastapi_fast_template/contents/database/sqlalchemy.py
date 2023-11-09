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
async_session = sessionmaker(
    autocommit = False, 
    autoflush = False,
    expire_on_commit = False, 
    bind = engine, 
    class_ = AsyncSession
)
Base = declarative_base()


async def get_session() -> AsyncSession:
    db_session = async_session()
    try:
        yield db_session
    finally:
        await db_session.close()