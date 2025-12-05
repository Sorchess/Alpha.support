from faststream.rabbit import RabbitBroker
from config import settings


def create_broker() -> RabbitBroker:
    """Фабрика для создания экземпляра брокера"""
    return RabbitBroker(url=str(settings.broker.url), reconnect_interval=5)


broker = create_broker()
