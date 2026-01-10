from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from core.security import generate_uuid


class Base(DeclarativeBase):
    """Базовый класс, нужен для опредения таблиц в базе данных, он хранит все метаданные"""

    __abstract__ = True  # Не создает таблицу в бд
    oid: Mapped[str] = mapped_column(
        String(255),
        primary_key=True,
        unique=True,
        index=True,
        default=generate_uuid,
    )
