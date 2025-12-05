from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.database.models import Base

if TYPE_CHECKING:
    from .user import User
    from .topic import Topic


class File(Base):
    __tablename__ = "files"

    key: Mapped[str] = mapped_column(String(255), nullable=False)
    origin: Mapped[str] = mapped_column(String(255))
    size: Mapped[int] = mapped_column(Integer)
    topic_oid: Mapped[str] = mapped_column(
        ForeignKey("topics.oid", ondelete="CASCADE"), nullable=True
    )
    owner_oid: Mapped[str] = mapped_column(
        ForeignKey("users.oid", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    topic: Mapped["Topic"] = relationship(
        "Topic",
        back_populates="files",
    )
    owner: Mapped["User"] = relationship(
        "User",
        back_populates="files",
    )
