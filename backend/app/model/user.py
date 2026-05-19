from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .timeline_members import timeline_members


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String())
    hashed_password: Mapped[str] = mapped_column(String())
    first_name: Mapped[str] = mapped_column(String(), nullable=True)
    last_name: Mapped[str] = mapped_column(String(), nullable=True)
    # timelines = relationship(
    #     "Timeline",
    #     uselist=True,
    #     back_populates="user"
    # )
    owned_timelines = relationship(
        "Timeline",
        uselist=True,
        back_populates="owner",
        lazy="selectin"
    )
    timeline_membership = relationship(
        "Timeline",
        uselist=True,
        secondary=timeline_members,
        back_populates="members",
        lazy="selectin"
    )

