from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)

from config import settings
from infra.database.models import Base


class DatabaseFactory:
    """Класс помощник который устанавливает соединение с базой данных и предоставляет сессию"""

    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def init_database(self):
        async with self.engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def dispose(
        self,
    ) -> None:
        """Закрывает все соединения пула и останавливает движок"""
        await self.engine.dispose()

    async def session_getter(
        self,
    ) -> AsyncSession:
        """Получение сессии для обработки запросов к базе данных"""
        async with self.session_factory() as session:
            yield session


db_factory = DatabaseFactory(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)
