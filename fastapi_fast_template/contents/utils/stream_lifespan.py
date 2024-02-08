@asynccontextmanager
async def stream_lifespan():
    await start_application()

    yield

    await down_application()
