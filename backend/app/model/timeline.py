from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base


class Timeline(Base):

    __tablename__ = "timelines"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user = relationship(
        "User",
        back_populates="timelines"
    )
    events = relationship(
        "Event",
        back_populates="timeline",
        uselist=True
    )