from typing import TYPE_CHECKING
from datetime import date

from sqlalchemy import ForeignKey, String, DATE
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.model.attachment import Attachment
from backend.app.model.base import Base

if TYPE_CHECKING:
    from backend.app.model.timeline import Timeline

class Event(Base):

    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String())
    event_date: Mapped[date] = mapped_column(
        DATE,
    )
    location: Mapped[str] = mapped_column(String(), nullable=True)
    description: Mapped[str] = mapped_column(String(), nullable=True)
    timeline_id: Mapped[int] = mapped_column(ForeignKey("timelines.id"))

    timeline: Mapped["Timeline"] = relationship(
        back_populates="events"
    )
    attachments: Mapped[list["Attachment"]] = relationship(
        back_populates="event",
        cascade="all, delete-orphan",
        order_by=Attachment.sort_order,
        lazy="selectin"
    )

