from abc import ABC, abstractmethod


class BasePublisher(ABC):

    @abstractmethod
    async def publish(self, message): ...
