from typing import Annotated


from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import HTMLResponse, FileResponse

from backend.app.model.attachment import Attachment
from backend.app.core.exceptions import NotFoundException
from backend.app.core.utils.permission import check_member_permission
from backend.app.schema.attachment import AttachmentResponseSchema, AttachmentCreateSchema
from backend.app.service.attachment import AttachmentService, get_attachment_service


router = APIRouter(
    prefix="/attachment",
)


@router.post(
    "/",
    response_model=AttachmentResponseSchema,
    status_code=201,
)
async def create_attachment(
        create_data: AttachmentCreateSchema,
        file: Annotated[UploadFile, File(description="A file read as UploadFile")],
        attachment_service: AttachmentService = Depends(get_attachment_service),
):
    attachment = await attachment_service.create_attachment(file, create_data)
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
        _member_permission = Depends(check_member_permission)
):
    attachment = await attachment_service.retrieve_one(Attachment.id, attachment_id)
    if not attachment:
        raise NotFoundException
    return attachment
