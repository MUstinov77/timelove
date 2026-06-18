from backend.app.core.auth.request_validator import authenticate_user
from fastapi import Depends
from backend.app.service.member import MemberService, get_member_service
from backend.app.service.timeline import TimelineService, get_timeline_service
from backend.app.core.exceptions import NotFoundException, PermissionException
from backend.app.core.enum.permission import MemberPermission
from backend.app.model.timeline import Timeline


async def get_member_permission(
        timeline_id: int,
        auth_user: dict = Depends(authenticate_user),
        member_service: MemberService = Depends(get_member_service),
):
    user_id = auth_user.get("user_id")
    membership = await member_service.retrieve_membership(timeline_id, user_id)
    if not membership:
        raise PermissionException
    return membership.member_permission


async def check_member_permission(
        member_permission: MemberPermission = Depends(get_member_permission)
):
    return member_permission


async def check_moder_permission(
        member_permission: MemberPermission = Depends(get_member_permission)
):
    if member_permission == MemberPermission.MEMBER:
        raise PermissionException
    return True

async def check_admin_permission(
        member_permission: MemberPermission = Depends(get_member_permission)
):
    if member_permission != MemberPermission.ADMIN:
        raise PermissionException
    return True