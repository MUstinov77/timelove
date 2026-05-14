from fastapi import APIRouter, Depends

from backend.app.core.exceptions import NotFoundException
from backend.app.model.event import Event
from backend.app.model.user import User
from backend.app.schema.event import EventCreateUpdateSchema, EventResponseSchema
from backend.app.service.event import EventService, get_event_service

router = APIRouter(
    prefix="/event",
)

@router.get(
    "/{event_id}",
    response_model=EventResponseSchema,
)
async def get_event(
        event_id: int,
        event_service: EventService = Depends(get_event_service)
):
    event = await event_service.retrieve_one(Event.id, event_id)
    if not event:
        raise NotFoundException
    return event

@router.get(
    "/",
    response_model=list[EventResponseSchema]
)
async def get_my_events(
        event_service: EventService = Depends(get_event_service)
):
    events = await event_service.retrieve_all(User.id, 1)
    if not events:
        raise NotFoundException
    return events

@router.post(
    "/",
    response_model=EventResponseSchema,
)
async def create_event(
        create_data: EventCreateUpdateSchema,
        event_service: EventService = Depends(get_event_service)
):
    event = await event_service.create_instance(create_data.model_dump())
    if not event:
        raise NotFoundException
    return event

@router.patch(
    "/{event_id}",
    response_model=EventResponseSchema
)
async def update_event(
        update_data: EventCreateUpdateSchema,
        event_id: int,
        event_service: EventService = Depends(get_event_service)
):
    event = await event_service.update_instance(update_data.model_dump(), event_id)
    if not event:
        raise NotFoundException
    return event

@router.delete("/{event_id}")
async def delete_event(
        event_id: int,
        event_service: EventService = Depends(get_event_service)
):
    event = await event_service.delete_instance(event_id)
    if not event:
        raise NotFoundException
    return event
