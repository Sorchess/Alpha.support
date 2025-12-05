from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.database.models import Base


if TYPE_CHECKING:
    from .topic import Topic
    from .user import User


class Message(Base):
    __tablename__ = "messages"

    content: Mapped[str] = mapped_column(String(1024), nullable=False)
    author_oid: Mapped[str] = mapped_column(
        ForeignKey("users.oid", ondelete="CASCADE"), nullable=False
    )
    topic_oid: Mapped[str] = mapped_column(
        ForeignKey("topics.oid", ondelete="CASCADE"), nullable=False
    )
    sended_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now,
    )
    # Relationships
    author: Mapped["User"] = relationship(
        "User",
        back_populates="messages",
    )
    topic: Mapped["Topic"] = relationship(
        "Topic",
        back_populates="messages",
    )
