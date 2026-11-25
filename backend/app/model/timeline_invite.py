from datetime import datetime
from uuid import UUID, uuid7

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.enum.permission import MemberPermission

from .base import Base


class TimelineInvite(Base):
    """A pending invitation to join a timeline."""

    __tablename__ = "timeline_invites"
    __table_args__ = (
        CheckConstraint(
            "sender_id <> receiver_id",
            name="ck_timeline_invites_different_users",
        ),
        UniqueConstraint("timeline_id", "receiver_id", name="uq_timeline_invites_recipient"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True, default=uuid7)
    timeline_id: Mapped[int] = mapped_column(ForeignKey("timelines.id", ondelete="CASCADE"))
    sender_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    receiver_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    member_permission: Mapped[MemberPermission] = mapped_column(
        SAEnum(
            MemberPermission,
            name="member_permission_enum",
            values_callable=lambda enum: [member.value for member in enum],
        ),
        default=MemberPermission.MEMBER,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.current_timestamp(),
    )
