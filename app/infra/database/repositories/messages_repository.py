from .base_repository import BaseRepository
from infra.database.models import Message
from schemas.message import MessageResponse


class MessagesRepository(BaseRepository):
    model = Message
    schema = MessageResponse
