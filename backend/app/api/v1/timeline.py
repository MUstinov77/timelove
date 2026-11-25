from fastapi import APIRouter, Depends, Response, status

from backend.app.api.v1.event import router as event_router
from backend.app.core.enum.permission import MemberPermission
from backend.app.core.exceptions import NotFoundException
from backend.app.dependencies.auth import AuthUserDep, authenticate_user
from backend.app.dependencies.permission import (
    AdminPermissionDep,
    MemberPermissionDep,
    ModeratorPermissionDep,
)
from backend.app.dependencies.service import MemberServiceDep, TimelineServiceDep, TimelineInviteDep
from backend.app.schema.timeline import InviteUserToTimelineSchema
from backend.app.schema.timeline import (
    TimelineCreateUpdateSchema,
    TimelineResponseSchema,
)

router = APIRouter(
    prefix="/timeline",
    dependencies=(
        Depends(authenticate_user),
    )
)

router.include_router(
    event_router,
    prefix="/{timeline_id}"
)


@router.get(
    "/",
    response_model=list[TimelineResponseSchema]
)
async def get_my_timelines(
    timeline_service: TimelineServiceDep,
    user_id: AuthUserDep,
):
    timelines = await timeline_service.get_timelines_by_user_id(user_id)
    return timelines


@router.post(
    "/",
    response_model=TimelineResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_timeline(
    create_data: TimelineCreateUpdateSchema,
    timeline_service: TimelineServiceDep,
    member_service: MemberServiceDep,
    user_id: AuthUserDep,
):
    timeline_data = create_data.model_dump()
    timeline = await timeline_service.create(timeline_data)
    if not timeline:
        raise NotFoundException
    member_create_data = InviteUserToTimelineSchema(
        member_id=user_id,
        member_permission=MemberPermission.ADMIN
    ).model_dump()
    member_create_data["timeline_id"] = timeline.id
    await member_service.create(member_create_data)
    return TimelineResponseSchema(
        id=timeline.id,
        title=timeline.title,
        member_permission=MemberPermission.ADMIN,
    )

# add some logic to acceptable invite(create invite instance)
@router.post(
    "/{timeline_id}/invite"
)
async def invite_user_to_timeline(
        timeline_id: int,
        invite_data: InviteUserToTimelineSchema,
        timeline_invite_service: TimelineInviteDep,
        _moder_permission: ModeratorPermissionDep,
        user_id: AuthUserDep
):
    invite_create_data = invite_data.model_dump()
    invite_create_data["timeline_id"] = timeline_id
    invite_create_data["sender_id"] = user_id
    invite_create_data["member_permission"] = MemberPermission.MEMBER
    await timeline_invite_service.create(invite_create_data)
    return {"message": "User invited to timeline"}


@router.get(
    "/{timeline_id}",
    response_model=TimelineResponseSchema
)
async def get_timeline(
        timeline_id: int,
        timeline_service: TimelineServiceDep,
        user_id: AuthUserDep,
        _member_permission: MemberPermissionDep
):
    timeline = await timeline_service.retrieve_timeline(timeline_id, user_id)
    if not timeline:
        raise NotFoundException
    return timeline


@router.patch(
    "/{timeline_id}",
    response_model=TimelineResponseSchema,
)
async def update_timeline(
    timeline_id: int,
    update_data: TimelineCreateUpdateSchema,
    timeline_service: TimelineServiceDep,
    member_permission: MemberPermissionDep
):
    timeline = await timeline_service.update_instance(update_data.model_dump(), timeline_id)
    if not timeline:
        raise NotFoundException
    return TimelineResponseSchema(
        id=timeline.id,
        title=timeline.title,
        member_permission=member_permission,
    )


@router.delete(
    "/{timeline_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_timeline(
    timeline_id: int,
    timeline_service: TimelineServiceDep,
    _admin_permission: AdminPermissionDep
):
    timeline = await timeline_service.delete(timeline_id)
    if not timeline:
        raise NotFoundException
    return Response(status_code=status.HTTP_204_NO_CONTENT)
