from sqlalchemy import ForeignKey, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.enum.permission import MemberPermission
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
    member_permission: Mapped[MemberPermission] = mapped_column(
        SAEnum(
            MemberPermission,
            name="member_permission_enum",
            values_callable=lambda e: [m.value for m in e]
        ),
        default=MemberPermission.MEMBER,
    )
    member_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        primary_key=True
    )
