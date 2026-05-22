from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Timeline(Base):

    __tablename__ = "timelines"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # member_ids: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # user = relationship(
    #     "User",
    #     back_populates="timelines"
    # )
    events = relationship(
        "Event",
        back_populates="timeline",
        uselist=True
    )

    owner = relationship(
        "User",
        back_populates="owned_timelines"
    )
    members = relationship(
        "TimelineMembers",
        back_populates="timeline",
        lazy="selectin"
    )