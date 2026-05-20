from sqlalchemy import Column, ForeignKey, Integer, Table, Enum

from backend.app.core.enum.permission import MemberPermission
from .base import Base

timeline_members = Table(
    "timeline_members",
    Base.metadata,
    Column(
        "timeline_id",
        Integer,
        ForeignKey("timelines.id"),
    ),
    Column(
        "member_permission",
        Enum(MemberPermission),
        default=MemberPermission.DEFAULT,
    ),
    Column(
        "member_id",
        Integer,
        ForeignKey("users.id"),
    )
)