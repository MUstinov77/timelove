from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from .base import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(
        String()
    )
    surname: Mapped[str] = mapped_column(
        String()
    )

    timelines = relationship(
        "Timeline",
        uselist=True,
        back_populates="user"
    )

