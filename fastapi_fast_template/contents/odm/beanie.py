import motor.motor_asyncio
from beanie import init_beanie
from pydantic import MongoDsn


async def init_database(
    mongo_connection: MongoDsn,
    mongo_db: str,
):
    client = motor.motor_asyncio.AsyncIOMotorClient(str(mongo_connection))
    await init_beanie(
        database=client[mongo_db],
        document_models=[],  # models.Model
    )
