from config import settings
from tortoise import Tortoise


async def init_db(generate_schemas: bool = False):
    await Tortoise.init(
        db_url=settings.tortoise_db_url,
        modules={
            "models": [
                # models.module
            ]
        },
        timezone="Asia/Tehran",
    )
    if generate_schemas:
        await Tortoise.generate_schemas()


async def close_db():
    await Tortoise.close_connections()
