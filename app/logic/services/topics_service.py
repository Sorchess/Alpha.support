from dataclasses import dataclass

from core.exceptions import (
    ObjectAlreadyExistsException,
    TopicAlreadyExistsException,
    ObjectNotFoundException,
    TopicNotFoundException,
)
from logic.services.base_service import BaseService
from schemas.topic import TopicCreate, TopicResponse, TopicDB


@dataclass(eq=False, frozen=True)
class TopicsService(BaseService):

    async def get_topics(self, user_oid: str) -> list[TopicResponse]:
        try:
            return await self.db.topics.get_all(author_oid=user_oid)
        except ObjectNotFoundException:
            raise TopicNotFoundException

    async def upload_topic(
        self, user_oid: str, topic_create: TopicCreate
    ) -> TopicResponse:
        topic = TopicDB(
            title=topic_create.title,
            description=topic_create.description,
            author_oid=user_oid,
        )

        try:
            return await self.db.topics.add(schema=topic)
        except ObjectAlreadyExistsException:
            raise TopicAlreadyExistsException
