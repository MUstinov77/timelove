from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from backend.app.api.v1.event import router as event_router
from backend.app.core.auth.request_validator import authenticate_user
from backend.app.core.enum.permission import MemberPermission
from backend.app.core.exceptions import NotFoundException
from backend.app.core.utils.permission import check_permission_dependency
from backend.app.model.timeline import Timeline
from backend.app.model.user import User
from backend.app.schema.member import InviteUserToTimelineSchema
from backend.app.schema.timeline import (TimelineCreateUpdateSchema,
                                         TimelineResponseSchema)
from backend.app.service.member import MemberService, get_member_service
from backend.app.service.timeline import TimelineService, get_timeline_service
from backend.app.service.user import UserService, get_user_service

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

# @router.get("/attachments")
# async def upload_attachment():
#     content = """
# <body>
# <form action="/timeline/1/event/4/attachment/?caption=Some caption" enctype="multipart/form-data" method="post">
# <input name="file" type="file" multiple>
# <input type="submit">
# </form>
# <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# </body>
#     """
#     return HTMLResponse(content=content)


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
    timeline = await timeline_service.create(timeline_data)
    if not timeline:
        raise NotFoundException
    member_create_data = InviteUserToTimelineSchema(
        member_id=user_id,
        member_permission=MemberPermission.ADMIN
    ).model_dump()
    member_create_data["timeline_id"] = timeline.id
    await member_service.create(member_create_data)
    return timeline


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
    _moder_permission = Depends(check_permission_dependency(MemberPermission.MODERATOR))
):
    timeline = await timeline_service.update_instance(update_data.model_dump(), timeline_id)
    if not timeline:
        raise NotFoundException
    return timeline


@router.delete("/{timeline_id}")
async def delete_timeline(
    timeline_id: int,
    timeline_service: TimelineService = Depends(get_timeline_service),
    _admin_permission = Depends(check_permission_dependency(MemberPermission.ADMIN))
):
    timeline = await timeline_service.delete_instance(timeline_id)
    if not timeline:
        raise NotFoundException
    return timeline
