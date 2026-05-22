from pydantic import BaseModel

from backend.app.core.enum.permission import MemberPermission




class InviteUserToTimelineSchema(BaseModel):
    member_id: int
    member_permission: MemberPermission
