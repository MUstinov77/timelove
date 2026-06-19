from fastapi import APIRouter, Depends

from backend.app.core.enum.permission import MemberPermission
from backend.app.core.auth.request_validator import authenticate_user
from backend.app.core.exceptions import NotFoundException
from backend.app.model.timeline import Timeline
from backend.app.model.user import User
from backend.app.schema.timeline import (TimelineCreateUpdateSchema,
                                         TimelineResponseSchema)
from backend.app.service.timeline import TimelineService, get_timeline_service
from backend.app.service.user import UserService, get_user_service
from backend.app.core.utils.permission import check_member_permission, check_admin_permission, check_moder_permission, check_permission_dependency
from backend.app.schema.member import InviteUserToTimelineSchema
from backend.app.service.member import MemberService, get_member_service
from backend.app.schema.event import EventResponseSchema



router = APIRouter(
    prefix="/timeline",
    dependencies=(
        Depends(authenticate_user),
    )
)


@router.get(
    "/",
    response_model=list[TimelineResponseSchema]
)
async def get_my_timelines(
    auth_user = Depends(authenticate_user),
    user_service: UserService = Depends(get_user_service),
):
    user_id = auth_user.get("user_id")
    user = await user_service.retrieve_one(User.id, user_id)
    if not user:
        raise NotFoundException
    return user.timelines


@router.post(
    "/",
    response_model=TimelineResponseSchema,
)
async def create_timeline(
    create_data: TimelineCreateUpdateSchema,
    auth_user = Depends(authenticate_user),
    timeline_service: TimelineService = Depends(get_timeline_service),
    member_service: MemberService = Depends(get_member_service),
):
    user_id = auth_user.get("user_id")
    timeline_data = create_data.model_dump()
    timeline = await timeline_service.create_instance(timeline_data)
    if not timeline:
        raise NotFoundException
    member_create_data = InviteUserToTimelineSchema(
        member_id=user_id,
        member_permission=MemberPermission.ADMIN
    ).model_dump()
    member_create_data["timeline_id"] = timeline.id
    await member_service.create_instance(member_create_data)
    return timeline


@router.post(
    "/{timeline_id}/invite"
)
async def invite_user_to_timeline(
        timeline_id: int,
        invite_data: InviteUserToTimelineSchema,
        member_service: MemberService = Depends(get_member_service),
        _moder_permission = Depends(check_moder_permission)
):
    membership_data = invite_data.model_dump()
    membership_data["timeline_id"] = timeline_id
    await member_service.create_instance(membership_data)
    return {"message": "User invited to timeline"}

@router.get(
    "/{timeline_id}/events",
    response_model=list[EventResponseSchema]
)
async def get_timeline_events(
        timeline_id: int,
        timeline_service: TimelineService = Depends(get_timeline_service),
        _member_permission = Depends(check_permission_dependency(MemberPermission.MEMBER))
):
    timeline = await timeline_service.retrieve_one(Timeline.id, timeline_id)
    if not timeline:
        raise NotFoundException
    return timeline.events


@router.get(
    "/{timeline_id}",
    response_model=TimelineResponseSchema
)
async def get_timeline(
        timeline_id: int,
        timeline_service: TimelineService = Depends(get_timeline_service),
        _member_permission = Depends(check_member_permission)
):
    timeline = await timeline_service.retrieve_one(Timeline.id, timeline_id)
    if not timeline:
        raise NotFoundException
    return timeline


@router.patch(
    "/{timeline_id}",
    response_model=TimelineResponseSchema
)
async def update_timeline(
    timeline_id: int,
    update_data: TimelineCreateUpdateSchema,
    timeline_service: TimelineService = Depends(get_timeline_service),
    _moder_permission = Depends(check_moder_permission)
):
    timeline = await timeline_service.update_instance(update_data.model_dump(), timeline_id)
    if not timeline:
        raise NotFoundException
    return timeline


@router.delete("/{timeline_id}")
async def delete_timeline(
    timeline_id: int,
    timeline_service: TimelineService = Depends(get_timeline_service),
    _admin_permission = Depends(check_admin_permission)
):
    timeline = await timeline_service.delete_instance(timeline_id)
    if not timeline:
        raise NotFoundException
    return timeline
