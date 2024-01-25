import os
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import settings

from fastapi_fast_template.utils.enums import FileEnum
from fastapi_fast_template.utils.helpers import create_file

scheduler = AsyncIOScheduler()


def start_scheduler():
    if settings.enable_scheduler:
        create_file(FileEnum.LAST_RUN_SCHEDULER)
        last_run = datetime.fromtimestamp(
            os.path.getmtime(FileEnum.LAST_RUN_SCHEDULER)
        )
        if datetime.now() - last_run > timedelta(seconds=5):
            with open(FileEnum.LAST_RUN_SCHEDULER, "w") as f:
                f.write(str(datetime.now()))

            scheduler.start()


def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown()
