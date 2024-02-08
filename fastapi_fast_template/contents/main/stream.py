from faststream import FastStream
{import_faststream_broker}

from src.utils.lifespan import stream_lifespan
from src.config import settings

broker = {faststream_broker}(settings.broker_url)
app = FastStream(
    broker,
    lifespan=stream_lifespan,
)


@broker.subscriber("test")
async def handle() -> str:
    return "Hi!"
