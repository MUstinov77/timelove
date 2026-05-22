from backend.app.core.auth.request_validator import authenticate_user
from fastapi import Depends
from backend.app.service.member import MemberService, get_member_service
from backend.app.service.timeline import TimelineService, get_timeline_service
from backend.app.core.exceptions import NotFoundException, PermissionException
from backend.app.core.enum.permission import MemberPermission
from backend.app.model.timeline import Timeline


async def check_member_permission(
        timeline_id: int,
        user_credentials: dict = Depends(authenticate_user),
        timeline_service: TimelineService = Depends(get_timeline_service),
        member_service: MemberService = Depends(get_member_service),
):
    user_id: int = user_credentials.get("user_id")
    timeline = await timeline_service.retrieve_one(Timeline.id, timeline_id)
    if not timeline:
        raise NotFoundException
    if timeline.owner_id == user_id:
        return True
    membership = await member_service.retrieve_membership(timeline_id, user_id)
    if not membership or membership.member_permission != MemberPermission.CHANGE:
        raise PermissionException

    return True
