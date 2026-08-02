from fastapi import Depends

from backend.app.core.enum.permission import MemberPermission
from backend.app.core.exceptions import NotFoundException
from backend.app.core.utils.permission import check_permission_dependency
from backend.app.model.event import Event
from backend.app.service.event import EventService, get_event_service


async def retrieve_event(
        timeline_id: int,
        event_id: int,
        _member_permission = Depends(check_permission_dependency(MemberPermission.MEMBER)),
        event_service: EventService = Depends(get_event_service)
):
    event = await event_service.retrieve_one(Event.id, event_id)
    if not event:
        raise NotFoundException
    return event