from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException

from backend.app.schema.attachment import AttachmentCreateSchema
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

@router.get(
    "/",
    response_model=list[AttachmentResponseSchema]
)
async def get_attachments(
        timeline_id: int,
        event_id: int,
        event = Depends(retrieve_event),
        _member_permission = Depends(check_permission_dependency(MemberPermission.MEMBER)),
):
    if not event:
        raise NotFoundException
    return event.attachments

@router.post(
    "/",
    response_model=AttachmentResponseSchema,
)
async def create_attachment(
        timeline_id: int,
        caption: str | None = "",
        file: UploadFile = File(...),
        event = Depends(retrieve_event),
        attachment_service: AttachmentService = Depends(get_attachment_service),
        _moder_permission = Depends(check_permission_dependency(MemberPermission.MODERATOR)),
):
    sort_order = len(event.attachments) + 1 if event.attachments else 0
    request_data = {
        "caption": "Это вложение",
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
        timeline_id: int,
        attachment_id: int,
        event_id: int,
        attachment_service: AttachmentService = Depends(get_attachment_service),
        _member_permission = Depends(check_permission_dependency(MemberPermission.MEMBER))
):
    attachment = await attachment_service.retrieve_one(Attachment.id, attachment_id)
    if not attachment:
        raise NotFoundException
    return attachment


@router.patch(
    "/{attachment_id}",
    response_model=AttachmentResponseSchema,
)
async def update_attachment(
        timeline_id: int,
        attachment_id: int,
        event_id: int,
        update_data: AttachmentCreateSchema,
        attachment_service: AttachmentService = Depends(get_attachment_service),
        _moder_permission = Depends(check_permission_dependency(MemberPermission.MODERATOR))
):
    attachment = await attachment_service.update_instance(
        update_data.model_dump(),
        attachment_id
    )
    if not attachment:
        raise NotFoundException
    return attachment


@router.delete(
    "/{attachment_id}",
    status_code=204,
)
async def delete_attachment(
        timeline_id: int,
        attachment_id: int,
        event_id: int,
        attachment_service: AttachmentService = Depends(get_attachment_service),
        _moder_permission = Depends(check_permission_dependency(MemberPermission.MODERATOR))
):
    attachment = await attachment_service.delete_attachment(attachment_id)
    if not attachment:
        raise NotFoundException
    return attachment


@router.get(
    "/{attachment_id}/file",
)
async def get_attachment_file(
        timeline_id: int,
        attachment_id: int,
        event_id: int,
        attachment_service: AttachmentService = Depends(get_attachment_service),
        _member_permission = Depends(check_permission_dependency(MemberPermission.MEMBER))
):
    attachment = await attachment_service.retrieve_one_by_id(attachment_id)
    if not attachment:
        raise HTTPException(status_code=401, detail="Attachment not found")
    return FileResponse(attachment.storage_key)