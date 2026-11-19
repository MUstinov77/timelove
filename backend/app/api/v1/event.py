from fastapi import APIRouter, Response, status

from backend.app.api.v1.attachment import router as attachment_router
from backend.app.core.exceptions import NotFoundException
from backend.app.dependencies.permission import (
    AdminPermissionDep,
    MemberPermissionDep,
    ModeratorPermissionDep,
)
from backend.app.dependencies.service import EventServiceDep
from backend.app.schema.event import (
    EventCreateSchema,
    EventResponseSchema,
    EventUpdateSchema,
)

router = APIRouter(
    prefix="/event",
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
    event_service: EventServiceDep,
    _member_permission: MemberPermissionDep
):
    events = await event_service.retrieve_timeline_events(timeline_id)
    return events

@router.post(
    "/",
    response_model=EventResponseSchema,
)
async def create_event(
        timeline_id: int,
        create_data: EventCreateSchema,
        event_service: EventServiceDep,
        _moder_permission: ModeratorPermissionDep
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
        event_service: EventServiceDep,
        _member_permission: MemberPermissionDep
):
    event = await event_service.retrieve_event(timeline_id, event_id)
    if not event:
        raise NotFoundException
    return event


@router.patch(
    "/{event_id}",
    response_model=EventResponseSchema
)
async def update_event(
        timeline_id: int,
        event_id: int,
        update_data: EventUpdateSchema,
        event_service: EventServiceDep,
        _moder_permission: ModeratorPermissionDep
):
    event = await event_service.retrieve_event(timeline_id, event_id)
    if not event:
        raise NotFoundException
    event = await event_service.update_instance(update_data.model_dump(exclude_unset=True), event_id)
    return event


@router.delete("/{event_id}")
async def delete_event(
        timeline_id: int,
        event_id: int,
        event_service: EventServiceDep,
        _admin_permission: AdminPermissionDep
):
    event = await event_service.retrieve_event(timeline_id, event_id)
    if not event:
        raise NotFoundException
    await event_service.delete(event.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
