from sqlalchemy import ForeignKey, Column, Table, Integer

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
    ## TODO: ADD permisions to table
    # permision, type: strEnum(
    Column(
        "member_id",
        Integer,
        ForeignKey("users.id"),
    )
)