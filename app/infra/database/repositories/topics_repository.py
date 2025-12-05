from .base_repository import BaseRepository
from infra.database.models.topic import Topic
from schemas.topic import TopicResponse


class TopicsRepository(BaseRepository):
    model = Topic
    schema = TopicResponse
