from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.enum.permission import MemberPermission
from sqlalchemy import ForeignKey, UniqueConstraint, String

from backend.app.model.base import Base


class TimelineMembers(Base):

    __tablename__ = "timeline_members"

    timeline_id: Mapped[int] = mapped_column(
        ForeignKey(
            "timelines.id",
            ondelete="CASCADE",
        ),
        primary_key=True
    )
    member_permission: Mapped[str] = mapped_column(
        String,
        default=MemberPermission.MEMBER,
    )
    member_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    __table_args__ = (
        UniqueConstraint(
            "timeline_id",
            "member_id",
            name="unique_timeline_member"
        ),
    )