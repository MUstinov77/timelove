from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.enum.permission import MemberPermission
from sqlalchemy import Enum, ForeignKey, UniqueConstraint

from backend.app.model.base import Base

if TYPE_CHECKING:
    from backend.app.model.timeline import Timeline
    from backend.app.model.user import User

class TimelineMembers(Base):

    __tablename__ = "timeline_members"

    timeline_id: Mapped[int] = mapped_column(
        ForeignKey("timelines.id"),
        primary_key=True
    )
    member_permission: Mapped[str] = mapped_column(
        Enum(MemberPermission),
        default=MemberPermission.DEFAULT
    )
    member_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )

    __table_args__ = (
        UniqueConstraint(
            "timeline_id",
            "member_id",
            name="unique_timeline_member"
        ),
    )