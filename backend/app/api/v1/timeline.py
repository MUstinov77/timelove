from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from backend.app.core.auth.request_validator import authenticate_user
from backend.app.core.exceptions import NotFoundException
from backend.app.model.timeline import Timeline
from backend.app.model.user import User
from backend.app.schema.timeline import (TimelineCreateUpdateSchema,
                                         TimelineResponseSchema)
from backend.app.service.timeline import TimelineService, get_timeline_service
from backend.app.service.user import UserService, get_user_service

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
    user_credentials = Depends(authenticate_user),
    user_service: UserService = Depends(get_user_service)
):
    user = await user_service.retrieve_one(User.id, user_credentials.get("user_id"))
    if not user:
        raise NotFoundException
    return user.owned_timelines + user.timeline_membership


@router.post(
    "/invite/{user_id}"
)
async def invite_user_to_timeline(
        user_id: int,
        user_service: UserService = Depends(get_user_service)
):
    user = await user_service.retrieve_one(User.id, user_id)
    if not user:
        raise NotFoundException
    user.timeline_membership.append(user)
    return {"message": "User invited to timeline"}


@router.get(
    "/{timeline_id}",
    response_model=TimelineResponseSchema
)
async def get_timeline(
    timeline_id: int,
    timeline_service: TimelineService = Depends(get_timeline_service)
):
    timeline = await timeline_service.retrieve_one(Timeline.id, timeline_id)
    if not timeline:
        raise NotFoundException
    return timeline

@router.post(
    "/",
    response_model=TimelineResponseSchema,
)
async def create_timeline(
    create_data: TimelineCreateUpdateSchema,
    user_credentials = Depends(authenticate_user),
    timeline_service: TimelineService = Depends(get_timeline_service)
):
    timeline_data = create_data.model_dump()
    timeline_data["owner_id"] = user_credentials["user_id"]
    timeline = await timeline_service.create_instance(timeline_data)
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
    user_credentials = Depends(authenticate_user),
    timeline_service: TimelineService = Depends(get_timeline_service)
):
    timeline = await timeline_service.update_instance(update_data.model_dump(), timeline_id)
    if user_credentials.get("user_id") != timeline.owner_id:
        raise HTTPException(status_code=403, detail="You are not the owner of this timeline")
    if not timeline:
        raise NotFoundException
    return timeline


@router.delete("/{timeline_id}")
async def delete_timeline(
    timeline_id: int,
    timeline_service: TimelineService = Depends(get_timeline_service)
):
    timeline = await timeline_service.delete_instance(timeline_id)
    if not timeline:
        raise NotFoundException
    return timeline
