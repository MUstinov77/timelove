from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.model.base import Base

if TYPE_CHECKING:
    from backend.app.model.timeline import Timeline



class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(), unique=True)
    hashed_password: Mapped[str] = mapped_column(String())
    first_name: Mapped[str] = mapped_column(String(), nullable=True)
    last_name: Mapped[str] = mapped_column(String(), nullable=True)
    # timelines = relationship(
    #     "Timeline",
    #     uselist=True,
    #     back_populates="user"
    # )
    timelines: Mapped[list["Timeline"]] = relationship(
        back_populates="members",
        secondary="timeline_members",
        lazy="selectin"
    )

