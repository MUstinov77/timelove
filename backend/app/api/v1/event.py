from fastapi import APIRouter, Depends, UploadFile, File

from backend.app.service.attachment import AttachmentService, get_attachment_service
from backend.app.schema.attachment import AttachmentResponseSchema
from backend.app.core.utils.permission import check_moder_permission
from backend.app.core.auth.request_validator import authenticate_user
from backend.app.core.exceptions import NotFoundException
from backend.app.model.event import Event
from backend.app.schema.event import (EventCreateUpdateSchema,
                                      EventResponseSchema)
from backend.app.service.event import EventService, get_event_service
from backend.app.shortcuts.event import retrieve_event


router = APIRouter(
    prefix="/event",
    dependencies=(
        Depends(authenticate_user),
    )
)


@router.post(
    "/",
    response_model=EventResponseSchema,
)
async def create_event(
        create_data: EventCreateUpdateSchema,
        event_service: EventService = Depends(get_event_service),
        _moder_permission = Depends(check_moder_permission),
):
    event_data = create_data.model_dump()
    event = await event_service.create_instance(event_data)
    if not event:
        raise NotFoundException
    return event


@router.get(
    "/{event_id}",
    response_model=EventResponseSchema,
)
async def get_event(
        event: Event = Depends(retrieve_event)
):
    return event


@router.patch(
    "/{event_id}",
    response_model=EventResponseSchema
)
async def update_event(
        event_id: int,
        update_data: EventCreateUpdateSchema,
        event_service: EventService = Depends(get_event_service),
        _moder_permission = Depends(check_moder_permission),
):
    event = await event_service.update_instance(update_data.model_dump(), event_id)
    if not event:
        raise NotFoundException
    return event

@router.delete("/{event_id}")
async def delete_event(
        event_id: int,
        event_service: EventService = Depends(get_event_service),
        _moder_permission = Depends(check_moder_permission),
):
    event = await event_service.delete_instance(event_id)
    if not event:
        raise NotFoundException
    return event

@router.get(
    "/{event_id}/attachments",
    response_model=list[AttachmentResponseSchema],
)
async def get_event_attachments(
        event = Depends(retrieve_event),
):
    return event.attachments


@router.post(
    "/{event_id}/attachments",
    response_model=AttachmentResponseSchema,
)
async def create_attachment(
        event_id: int,
        caption: str | None,
        file: UploadFile = File(...),
        attachment_service: AttachmentService = Depends(get_attachment_service),
):
    request_data = {
        "caption": caption,
        "event_id": event_id,
    }
    attachment = await attachment_service.create_attachment(file, request_data)
    if not attachment:
        raise NotFoundException
    return attachment