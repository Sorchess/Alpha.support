from sqlalchemy.ext.asyncio import AsyncSession

from infra.database.repositories.files_repository import FilesRepository
from infra.database.repositories import MessagesRepository
from infra.database.repositories.topics_repository import TopicsRepository
from infra.database.repositories import UsersRepository


class DatabaseManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        self.users = UsersRepository(self.session)
        self.files = FilesRepository(self.session)
        self.topics = TopicsRepository(self.session)
        self.messages = MessagesRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
