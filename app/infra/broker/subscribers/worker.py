import logging

from faststream import FastStream

from config import settings
from infra.broker.connection import broker
from .messages import router as messages
from .emails import router as emails

worker = FastStream(broker)
broker.include_router(messages)
broker.include_router(emails)


@worker.after_startup
async def configure_logging() -> None:
    logging.basicConfig(
        level=settings.logging.log_level_value,
        format=settings.logging.log_format,
        datefmt=settings.logging.date_format,
    )
