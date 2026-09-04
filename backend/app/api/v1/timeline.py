from fastapi import APIRouter, Depends, status

from backend.app.api.v1.event import router as event_router
from backend.app.core.auth.request_validator import authenticate_user
from backend.app.core.enum.permission import MemberPermission
from backend.app.core.exceptions import NotFoundException
from backend.app.core.utils.permission import check_permission_dependency
from backend.app.schema.member import InviteUserToTimelineSchema
from backend.app.schema.timeline import TimelineCreateUpdateSchema, TimelineResponseSchema
from backend.app.service.member import MemberService, get_member_service
from backend.app.service.timeline import TimelineService, get_timeline_service

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
    auth_user = Depends(authenticate_user),
    timeline_service: TimelineService = Depends(get_timeline_service),
):
    user_id = auth_user.get("user_id")
    timelines = await timeline_service.get_timelines_by_user_id(user_id)
    return timelines


@router.post(
    "/",
    response_model=TimelineResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_timeline(
    create_data: TimelineCreateUpdateSchema,
    auth_user = Depends(authenticate_user),
    timeline_service: TimelineService = Depends(get_timeline_service),
    member_service: MemberService = Depends(get_member_service),
):
    user_id = auth_user.get("user_id")
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
    "/{timeline_id}/add"
)
async def add_user_to_timeline(
        timeline_id: int,
        invite_data: InviteUserToTimelineSchema,
        member_service: MemberService = Depends(get_member_service),
        _moder_permission = Depends(check_permission_dependency(MemberPermission.MODERATOR))
):
    membership_data = invite_data.model_dump()
    membership_data["timeline_id"] = timeline_id
    await member_service.create(membership_data)
    return {"message": "User added to timeline"}


@router.get(
    "/{timeline_id}",
    response_model=TimelineResponseSchema
)
async def get_timeline(
        timeline_id: int,
        timeline_service: TimelineService = Depends(get_timeline_service),
        _member_permission = Depends(check_permission_dependency(MemberPermission.MEMBER))
):
    timeline = await timeline_service.retrieve_timeline(timeline_id)
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
    timeline_service: TimelineService = Depends(get_timeline_service),
    member_permission: MemberPermission = Depends(
        check_permission_dependency(MemberPermission.MODERATOR, return_permission=True)
    ),
):
    timeline = await timeline_service.update_instance(update_data.model_dump(), timeline_id)
    if not timeline:
        raise NotFoundException
    return TimelineResponseSchema(
        id=timeline.id,
        title=timeline.title,
        member_permission=member_permission,
    )


@router.delete("/{timeline_id}")
async def delete_timeline(
    timeline_id: int,
    timeline_service: TimelineService = Depends(get_timeline_service),
    _admin_permission = Depends(check_permission_dependency(MemberPermission.ADMIN))
):
    timeline = await timeline_service.delete(timeline_id)
    if not timeline:
        raise NotFoundException
    return timeline
