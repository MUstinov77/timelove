from backend.app.core.auth.request_validator import authenticate_user
from fastapi import Depends
from backend.app.service.member import MemberService, get_member_service
from backend.app.core.exceptions import NotFoundException, PermissionException
from backend.app.core.enum.permission import MemberPermission


async def check_member_permission(
        timeline_id: int,
        user_credentials: dict = Depends(authenticate_user),
        member_service: MemberService = Depends(get_member_service)
):
    member_permission = await member_service.retrieve_member_permission(timeline_id, user_credentials.get("user_id"))
    if not member_permission:
        raise NotFoundException
    match member_permission:
        case MemberPermission.CHANGE:
            return True
        case _:
            raise PermissionException
