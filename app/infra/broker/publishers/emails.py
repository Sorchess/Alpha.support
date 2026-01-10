from faststream.rabbit import RabbitBroker

from .base import BasePublisher


class EmailPublisher(BasePublisher):
    """Адаптер для публикации email-сообщений"""

    def __init__(self, broker: RabbitBroker, queue: str = "emails"):
        self._broker = broker
        self._queue = queue

    async def publish(self, message: dict) -> None:
        """Публикует email-задачу в очередь"""
        await self._broker.publish(queue=self._queue, message=message)
