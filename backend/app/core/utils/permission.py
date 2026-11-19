from fastapi import status
from fastapi.exceptions import HTTPException

from backend.app.core.enum.permission import MemberPermission
from backend.app.core.exceptions import PermissionException
from backend.app.dependencies.auth import AuthUserDep
from backend.app.dependencies.service import MemberServiceDep


def check_permission_dependency(
        required_permission: MemberPermission,
):
    async def dependency(
            timeline_id: int,
            member_service: MemberServiceDep,
            user_id: AuthUserDep,
    ):
        if not isinstance(required_permission, MemberPermission):
            raise TypeError(
                f"required_permission must be MemberPermission, got {required_permission!r}"
            )
        member_permission = await member_service.retrieve_membership(timeline_id, user_id)
        if not member_permission:
            raise PermissionException
        match_user_permission(member_permission, required_permission)

        return member_permission

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
