from datetime import datetime
from uuid import UUID, uuid7

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class FriendRequest(Base):

    __tablename__ = "friend_requests"

    id: Mapped[UUID] = mapped_column(
        Uuid(),
        primary_key=True,
        default=uuid7
    )
    sender_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        )
    )
    receiver_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        )
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.current_timestamp()
    )

    __table_args__ = (
        CheckConstraint(
            "sender_id <> receiver_id",
            name="ck_friend_requests_different_users",
        ),
        Index(
            "uq_friend_requests_user_pair",
            func.least(sender_id, receiver_id),
            func.greatest(sender_id, receiver_id),
            unique=True,
        ),
    )
