from datetime import date, datetime, timezone

from sqlalchemy import TIMESTAMP, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Event(Base):

    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String())
    event_date: Mapped[date] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(timezone.utc)
    )
    location: Mapped[str] = mapped_column(String(), nullable=True)
    description: Mapped[str] = mapped_column(String(), nullable=True)


    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    timeline_id: Mapped[int] = mapped_column(ForeignKey("timelines.id"))

    timeline = relationship(
        "Timeline",
        back_populates="events"
    )

