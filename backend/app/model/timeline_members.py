from sqlalchemy import Column, ForeignKey, Integer, Table

from .base import Base

## TODO: add cascade to table
timeline_members = Table(
    "timeline_members",
    Base.metadata,
    Column(
        "timeline_id",
        Integer,
        ForeignKey("timelines.id"),
    ),
    Column(
        "member_id",
        Integer,
        ForeignKey("users.id"),
    )
)