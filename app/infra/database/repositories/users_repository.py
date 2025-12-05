from infra.database.models import User
from .base_repository import BaseRepository
from schemas.user import UserResponse


class UsersRepository(BaseRepository):
    model = User
    schema = UserResponse
