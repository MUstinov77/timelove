from uuid import UUID

from pydantic import BaseModel

from backend.app.core.enum.permission import MemberPermission


class MemberTimelineSchema(BaseModel):
    member_id: UUID
    member_permission: MemberPermission
