from sqlalchemy import create
from sqlalchemy.engine import URL
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

engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


async def get_session() -> SessionLocal:
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        await db_session.close()