from fastapi import Depends, status
from fastapi.exceptions import HTTPException

from backend.app.core.auth.request_validator import authenticate_user
from backend.app.core.enum.permission import MemberPermission
from backend.app.core.exceptions import PermissionException
from backend.app.service.member import MemberService, get_member_service


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

def check_permission_dependency(
        permission: MemberPermission
):
    async def dependency(
            timeline_id: int,
            member_service: MemberService = Depends(get_member_service),
            auth_user: dict = Depends(authenticate_user),
    ):
        user_id = auth_user.get("user_id")
        membership = await member_service.retrieve_membership(timeline_id, user_id)
        if not membership:
            raise PermissionException
        return match_user_permission(membership.member_permission, permission)

    return dependency

def match_user_permission(
        user_permission: MemberPermission,
        necessary_permission: MemberPermission
):
    permissions_order = {
        MemberPermission.MEMBER: 0,
        MemberPermission.MODERATOR: 1,
        MemberPermission.ADMIN: 2,
    }
    necessary_permission_value = permissions_order.get(user_permission)
    user_permission_value = permissions_order.get(user_permission)
    if not necessary_permission_value or not user_permission_value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="I dont know this permission level")
    return user_permission_value >= necessary_permission_value