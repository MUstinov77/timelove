from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.model.base import Base

if TYPE_CHECKING:
    from backend.app.model.user import User
    from backend.app.model.event import Event
    from backend.app.model.timeline_members import TimelineMembers


class Timeline(Base):

    __tablename__ = "timelines"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(), nullable=False)
    events: Mapped[list["Event"]] = relationship(
        back_populates="timeline",
        lazy="selectin"
    )
    members: Mapped[list["User"]] = relationship(
        back_populates="timelines",
        secondary="timeline_members",
        # lazy="selectin"
    )