from dataclasses import dataclass

from core.exceptions import (
    ObjectAlreadyExistsException,
    ObjectNotFoundException,
    MessageAlreadyExistsException,
)
from infra.broker.publishers.messages import MessagePublisher
from logic.services.base_service import BaseService
from schemas.message import MessageCreate, MessageDB, MessageResponse


@dataclass(eq=False, frozen=True)
class MessagesService(BaseService):
    pub: MessagePublisher

    async def get_messages(
        self, user_oid: str, topic_oid: str
    ) -> list[MessageResponse]:
        return await self.db.messages.get_all(topic_oid=topic_oid)

    async def send_message(
        self, user_oid: str, topic_oid: str, message_create: MessageCreate
    ) -> MessageResponse:
        message = MessageDB(
            content=message_create.content,
            topic_oid=topic_oid,
            author_oid=user_oid,
        )

        try:
            sended_message = await self.db.messages.add(schema=message)
            await self.pub.publish(message=sended_message)
            return sended_message
        except ObjectAlreadyExistsException:
            raise MessageAlreadyExistsException
