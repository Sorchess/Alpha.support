from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from infra.broker.connection import broker
from infra.broker.publishers.emails import EmailPublisher
from infra.broker.publishers.messages import MessagePublisher
from infra.database.factory import db_factory
from infra.database.manager import DatabaseManager
from infra.redis.adapter import RedisAdapter
from infra.redis.client import RedisClientFactory
from infra.storage.adapter import S3Adapter
from infra.storage.client import S3ClientFactory


_s3_client_factory = S3ClientFactory()
_s3_adapter = S3Adapter(client=_s3_client_factory)

_redis_factory = RedisClientFactory(url=settings.redis.url)
_redis_client = _redis_factory.get_client(db_index=0)
_cache_adapter = RedisAdapter(redis=_redis_client, namespace="cache")

_email_publisher = EmailPublisher(broker=broker)
_message_publisher = MessagePublisher(broker=broker)


def get_s3() -> S3Adapter:
    """Singleton S3 адаптер для работы с файловым хранилищем"""
    return _s3_adapter


def get_cache() -> RedisAdapter:
    """Singleton Redis адаптер для кеширования"""
    return _cache_adapter


async def get_db(
    session: AsyncSession = Depends(db_factory.session_getter),
) -> DatabaseManager:
    """Менеджер базы данных с автоматическим закрытием сессии"""
    async with DatabaseManager(session=session) as db_manager:
        yield db_manager


def get_email_publisher() -> EmailPublisher:
    """Singleton publisher для отправки email через RabbitMQ"""
    return _email_publisher


def get_message_publisher() -> MessagePublisher:
    """Singleton publisher для отправки email через RabbitMQ"""
    return _message_publisher


S3Dep = Annotated[S3Adapter, Depends(get_s3)]
CacheDep = Annotated[RedisAdapter, Depends(get_cache)]
DBDep = Annotated[DatabaseManager, Depends(get_db)]
EmailPublisherDep = Annotated[EmailPublisher, Depends(get_email_publisher)]
MessagePublisherDep = Annotated[MessagePublisher, Depends(get_message_publisher)]
