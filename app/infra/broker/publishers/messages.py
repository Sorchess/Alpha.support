from faststream.rabbit import RabbitBroker

from .base import BasePublisher


class MessagePublisher(BasePublisher):
    """Адаптер для обработки сообщений"""

    def __init__(self, broker: RabbitBroker, queue: str = "messages"):
        self._broker = broker
        self._queue = queue

    async def publish(self, message: dict) -> None:
        """Публикует email-задачу в очередь"""
        await self._broker.publish(queue=self._queue, message=message)
