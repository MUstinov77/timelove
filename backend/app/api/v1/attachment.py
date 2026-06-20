from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import HTMLResponse

from backend.app.core.enum.permission import MemberPermission
from backend.app.core.exceptions import NotFoundException
from backend.app.core.utils.permission import check_permission_dependency
from backend.app.model.attachment import Attachment
from backend.app.schema.attachment import AttachmentResponseSchema
from backend.app.service.attachment import (AttachmentService,
                                            get_attachment_service)
from backend.app.shortcuts.event import retrieve_event

router = APIRouter(
    prefix="/attachment",
)


@router.post(
    "/",
    response_model=AttachmentResponseSchema,
)
async def create_attachment(
        caption: str | None,
        file: UploadFile = File(...),
        event = Depends(retrieve_event),
        attachment_service: AttachmentService = Depends(get_attachment_service),
):
    sort_order = len(event.attachments) + 1 if event.attachments else 0
    request_data = {
        "caption": caption,
        "event_id": event.id,
        "sort_order": sort_order,
    }
    attachment = await attachment_service.create_attachment(file, request_data)
    if not attachment:
        raise NotFoundException
    return attachment



@router.get(
    "/{attachment_id}",
    response_model=AttachmentResponseSchema,
)
async def get_attachment(
        attachment_id: int,
        attachment_service: AttachmentService = Depends(get_attachment_service),
        _member_permission = Depends(check_permission_dependency(MemberPermission.MEMBER))
):
    attachment = await attachment_service.retrieve_one(Attachment.id, attachment_id)
    if not attachment:
        raise NotFoundException
    return attachment


@router.delete(
    "/{attachment_id}",
    status_code=204,
)
async def delete_attachment(
        attachment_id: int,
        attachment_service: AttachmentService = Depends(get_attachment_service),
        _moder_permission = Depends(check_permission_dependency(MemberPermission.MODERATOR))
):
    attachment = await attachment_service.delete_attachment(attachment_id)
    if not attachment:
        raise NotFoundException
    return attachment
