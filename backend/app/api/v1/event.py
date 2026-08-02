from fastapi import APIRouter, Depends

from backend.app.api.v1.attachment import router as attachment_router
from backend.app.core.enum.permission import MemberPermission
from backend.app.core.exceptions import NotFoundException
from backend.app.core.utils.permission import check_permission_dependency
from backend.app.model.event import Event
from backend.app.schema.event import (EventCreateUpdateSchema,
                                      EventResponseSchema)
from backend.app.service.event import EventService, get_event_service
from backend.app.service.timeline import TimelineService, get_timeline_service

router = APIRouter(
    prefix="/event",
    dependencies=(
    )
)

router.include_router(
    attachment_router,
    prefix="/{event_id}",
)

@router.get(
    "/",
    response_model=list[EventResponseSchema]
)
async def get_events(
    timeline_id: int,
    timeline_service: TimelineService = Depends(get_timeline_service),
    _member_permission = Depends(check_permission_dependency(MemberPermission.MEMBER)),
):
    timeline = await timeline_service.retrieve_one_by_id(timeline_id)
    if not timeline:
        raise NotFoundException
    return timeline.events

@router.post(
    "/",
    response_model=EventResponseSchema,
)
async def create_event(
        timeline_id: int,
        create_data: EventCreateUpdateSchema,
        event_service: EventService = Depends(get_event_service),
        _moder_permission = Depends(check_permission_dependency(MemberPermission.MODERATOR)),
):
    event_data = create_data.model_dump()
    event_data["timeline_id"] = timeline_id
    event = await event_service.create(event_data)
    if not event:
        raise NotFoundException
    return event


@router.get(
    "/{event_id}",
    response_model=EventResponseSchema,
)
async def get_event(
        timeline_id: int,
        event_id: int,
        event_service: EventService = Depends(get_event_service),
        _member_permission = Depends(check_permission_dependency(MemberPermission.MEMBER)),
):
    event = await event_service.retrieve_one(Event.id, event_id)
    if not event:
        raise NotFoundException
    return event


@router.patch(
    "/{event_id}",
    response_model=EventResponseSchema
)
async def update_event(
        event_id: int,
        update_data: EventCreateUpdateSchema,
        event_service: EventService = Depends(get_event_service),
        _moder_permission = Depends(check_permission_dependency(MemberPermission.MODERATOR)),
):
    event = await event_service.update_instance(update_data.model_dump(), event_id)
    if not event:
        raise NotFoundException
    return event


@router.delete("/{event_id}")
async def delete_event(
        event_id: int,
        event_service: EventService = Depends(get_event_service),
        _admin_permission = Depends(check_permission_dependency(MemberPermission.ADMIN)),
):
    event = await event_service.delete(event_id)
    if not event:
        raise NotFoundException
    return event
