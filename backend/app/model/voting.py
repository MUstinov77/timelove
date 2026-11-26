from datetime import datetime
from uuid import UUID, uuid7

from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Voting(Base):
    __tablename__ = "votings"

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True, default=uuid7)
    timeline_id: Mapped[int] = mapped_column(
        ForeignKey("timelines.id", ondelete="CASCADE"),
        index=True,
    )
    created_by_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String())
    description: Mapped[str | None] = mapped_column(Text())
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.current_timestamp(),
    )
    ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
