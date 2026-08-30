
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse

from backend.app.core.enum.permission import MemberPermission
from backend.app.core.exceptions import NotFoundException
from backend.app.core.utils.permission import check_permission_dependency
from backend.app.model.event import Event
from backend.app.schema.attachment import AttachmentCreateSchema, AttachmentResponseSchema
from backend.app.service.attachment import AttachmentService, get_attachment_service
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
        attachment_service: AttachmentService = Depends(get_attachment_service),
        _member_permission = Depends(check_permission_dependency(MemberPermission.MEMBER)),
):
    attachments = await attachment_service.retrieve_event_attachments(timeline_id, event_id)
    if not attachments:
        raise NotFoundException
    return attachments

@router.post(
    "/",
    response_model=AttachmentResponseSchema,
)
async def create_attachment(
        data: AttachmentCreateSchema = Depends(AttachmentCreateSchema.as_form),
        file: UploadFile = File(...),
        event: Event = Depends(retrieve_event(MemberPermission.MODERATOR)),
        attachment_service: AttachmentService = Depends(get_attachment_service),
):
    sort_order = len(event.attachments) + 1

    create_data = data.model_dump()

    create_data["sort_order"] = sort_order
    create_data["event_id"] = event.id

    attachment = await attachment_service.create_attachment(file, create_data)
    if not attachment:
        raise NotFoundException
    return attachment


@router.get(
    "/{attachment_id}",
    response_model=AttachmentResponseSchema,
)
async def get_attachment(
        timeline_id: int,
        event_id: int,
        attachment_id: int,
        attachment_service: AttachmentService = Depends(get_attachment_service),
        _member_permission = Depends(check_permission_dependency(MemberPermission.MEMBER))
):
    attachment = await attachment_service.retrieve_attachment(timeline_id, event_id, attachment_id)
    if not attachment:
        raise NotFoundException
    return attachment


@router.patch(
    "/{attachment_id}",
    response_model=AttachmentResponseSchema,
)
async def update_attachment(
        timeline_id: int,
        event_id: int,
        attachment_id: int,
        update_data: AttachmentCreateSchema,
        attachment_service: AttachmentService = Depends(get_attachment_service),
        _moder_permission = Depends(check_permission_dependency(MemberPermission.MODERATOR))
):
    attachment = await attachment_service.update_attachment(
        timeline_id,
        event_id,
        attachment_id,
        update_data.model_dump()
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
        event_id: int,
        attachment_id: int,
        attachment_service: AttachmentService = Depends(get_attachment_service),
        _moder_permission = Depends(check_permission_dependency(MemberPermission.MODERATOR))
):
    attachment = await attachment_service.delete_attachment(timeline_id, event_id, attachment_id)
    if not attachment:
        raise NotFoundException
    return attachment


@router.get(
    "/{attachment_id}/file",
)
async def get_attachment_file(
        timeline_id: int,
        event_id: int,
        attachment_id: int,
        attachment_service: AttachmentService = Depends(get_attachment_service),
        _member_permission = Depends(check_permission_dependency(MemberPermission.MEMBER))
):
    attachment = await attachment_service.retrieve_attachment(
        timeline_id,
        event_id,
        attachment_id,
    )
    if not attachment:
        raise HTTPException(status_code=401, detail="Attachment not found")
    return FileResponse(attachment.storage_key)
