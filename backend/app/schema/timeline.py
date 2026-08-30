from pydantic import BaseModel

from backend.app.core.enum.permission import MemberPermission


class TimelineCreateUpdateSchema(BaseModel):

    title: str


class TimelineResponseSchema(BaseModel):
    id: int
    title: str
    member_permission: MemberPermission
