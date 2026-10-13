from fastapi import Depends, status
from fastapi.exceptions import HTTPException

from backend.app.core.auth.request_validator import authenticate_user
from backend.app.core.enum.permission import MemberPermission
from backend.app.core.exceptions import PermissionException
from backend.app.service.member import MemberService, get_member_service


def check_permission_dependency(
        required_permission: MemberPermission,
        return_permission: bool = False,
):
    async def dependency(
            timeline_id: int,
            member_service: MemberService = Depends(get_member_service),
            auth_user: dict = Depends(authenticate_user),
    ):
        if not isinstance(required_permission, MemberPermission):
            raise TypeError(
                f"required_permission must be MemberPermission, got {required_permission!r}"
            )
        user_id = auth_user.get("user_id")
        member_permission = await member_service.retrieve_membership(timeline_id, user_id)
        if not member_permission:
            raise PermissionException
        match_user_permission(member_permission, required_permission)
        if return_permission:
            return member_permission
        return True

    return dependency

def match_user_permission(
        user_permission: MemberPermission,
        required_permission: MemberPermission
):
    unknown_permission_type = -1
    permissions_order = {
        MemberPermission.MEMBER: 1,
        MemberPermission.MODERATOR: 2,
        MemberPermission.ADMIN: 3,
    }
    required_permission_value = permissions_order.get(
        required_permission, unknown_permission_type
    )
    user_permission_value = permissions_order.get(
        user_permission, unknown_permission_type
    )
    if (
        required_permission_value == unknown_permission_type
        or user_permission_value == unknown_permission_type
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unknown permission level",
        )
    if user_permission_value < required_permission_value:
        raise PermissionException
    return True
