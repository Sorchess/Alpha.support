import logging
import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import api_router
from config import settings
from infra.broker.connection import broker
from infra.database.factory import db_factory


logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
    datefmt=settings.logging.date_format,
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    await db_factory.init_database()  # Создание таблиц в бд
    await broker.start()  # Запуск брокера

    yield

    await broker.stop()  # Остановка брокера
    await db_factory.dispose()  # Остановка бд


app = FastAPI(
    title="Alpha.support",
    lifespan=lifespan,
)

origins = [
    "http://localhost:3000",
    "http://79.141.72.182:3000",
    "http://ims-monitor.ru",
    "https://ims-monitor.ru",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
        host="0.0.0.0",
        port=8000,
    )
