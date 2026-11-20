from uuid import UUID

from sqlalchemy import ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Friends(Base):

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )
    friend_id: Mapped[UUID] = mapped_column(
        Uuid(),
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )