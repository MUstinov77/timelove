from fastapi import APIRouter, Depends

from backend.app.core.enum.permission import MemberPermission
from backend.app.core.utils.permission import check_permission_dependency
from backend.app.core.auth.request_validator import authenticate_user
from backend.app.core.exceptions import NotFoundException
from backend.app.model.event import Event
from backend.app.schema.event import (EventCreateUpdateSchema,
                                      EventResponseSchema)
from backend.app.service.event import EventService, get_event_service
from backend.app.api.v1.attachment import router as attachment_router


router = APIRouter(
    prefix="/event",
    dependencies=(
        Depends(authenticate_user),
    )
)

router.include_router(
    attachment_router,
    prefix="/{event_id}",
)


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
    event = await event_service.create_instance(event_data)
    if not event:
        raise NotFoundException
    return event


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
        _moder_permission = Depends(check_permission_dependency(MemberPermission.ADMIN)),
):
    event = await event_service.delete_instance(event_id)
    if not event:
        raise NotFoundException
    return event
