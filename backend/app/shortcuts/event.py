from fastapi import Depends

from backend.app.core.enum.permission import MemberPermission
from backend.app.core.exceptions import NotFoundException
from backend.app.core.utils.permission import check_permission_dependency
from backend.app.service.event import EventService, get_event_service


async def retrieve_event(
        required_permission: MemberPermission,
):
    async def dependency(
            timeline_id: int,
            event_id: int,
            event_service: EventService = Depends(get_event_service),
            _check_user_permission = Depends(check_permission_dependency(required_permission))
    ):
        event = await event_service.retrieve_event(timeline_id, event_id)
        if not event:
            raise NotFoundException
        return event
    return dependency