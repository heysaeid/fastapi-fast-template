import os
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi_fast_template.utils.helpers import create_file
from fastapi_fast_template.utils.enums import FileEnum
from config import settings


scheduler = AsyncIOScheduler()


def start_scheduler():
    if settings.enable_scheduler:
        create_file(FileEnum.last_run_scheduler)
        last_run = datetime.fromtimestamp(
            os.path.getmtime(FileEnum.last_run_scheduler)
        )
        if datetime.now() - last_run > timedelta(seconds=5):
            with open(FileEnum.last_run_scheduler, "w") as f:
                f.write(str(datetime.now()))

            scheduler.start()


def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown()