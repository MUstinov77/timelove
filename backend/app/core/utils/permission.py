from backend.app.core.auth.request_validator import authenticate_user
from fastapi import Depends


async def check_member_permission(
        timeline_id: int,
        user_credentials: dict = Depends(authenticate_user),
        member_service: ... = ...,
):
    pass