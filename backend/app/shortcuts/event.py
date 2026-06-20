from fastapi import Depends

from backend.app.core.exceptions import NotFoundException
from backend.app.model.event import Event
from backend.app.service.event import EventService, get_event_service


async def retrieve_event(
        event_id: int,
        event_service: EventService = Depends(get_event_service)
):
    event = await event_service.retrieve_one(Event.id, event_id)
    if not event:
        raise NotFoundException
    return event