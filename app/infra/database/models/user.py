from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.security import generate_uuid
from infra.database.models import Base


if TYPE_CHECKING:
    from .file import File
    from .topic import Topic
    from .message import Message


DEFAULT_AVATAR_KEY = "default.webp"


class User(Base):
    """Класс для опредения таблицы users, наследуется от класса base, который хранит все метаданные"""

    __tablename__ = "users"
    username: Mapped[str] = mapped_column(
        String(32), index=True, nullable=False, default=generate_uuid
    )
    avatar: Mapped[str] = mapped_column(
        String(255), nullable=False, default=DEFAULT_AVATAR_KEY
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    registered_in: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now,
    )

    # Relationships
    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="author",
        cascade="all, delete-orphan",
    )
    topics: Mapped[list["Topic"]] = relationship(
        "Topic",
        back_populates="author",
        cascade="all, delete-orphan",
    )
    files: Mapped[list["File"]] = relationship(
        "File",
        back_populates="author",
        cascade="all, delete-orphan",
    )
