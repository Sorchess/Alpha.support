from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.database.models import Base


if TYPE_CHECKING:
    from .message import Message
    from .user import User
    from .file import File


class Topic(Base):
    __tablename__ = "topics"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(1024), nullable=False)
    author_oid: Mapped[str] = mapped_column(
        ForeignKey("users.oid", ondelete="CASCADE"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now,
    )

    # Relationships
    files: Mapped[list["File"]] = relationship(
        "File",
        back_populates="topic",
        cascade="all, delete-orphan",
    )
    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="topic",
        cascade="all, delete-orphan",
    )
    author: Mapped["User"] = relationship(
        "User",
        back_populates="topics",
    )
