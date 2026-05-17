from sqlalchemy import String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, Mapped, mapped_column

from datetime import date, datetime, timezone

from .base import Base


class Event(Base):

    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String())
    event_date: Mapped[date] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(timezone.utc)
    )
    description: Mapped[str] = mapped_column(String())


    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    timeline_id: Mapped[int] = mapped_column(ForeignKey("timelines.id"))

    timeline = relationship(
        "Timeline",
        back_populates="events"
    )

