import os
from typing import Annotated
from mimetypes import guess_type


from fastapi import APIRouter, UploadFile, File, Request, Query, Depends
from fastapi.responses import HTMLResponse

from backend.app.model.attachment import Attachment
from backend.app.core.exceptions import NotFoundException
from backend.app.core.utils.permission import check_member_permission
from backend.app.schema.attachment import AttachmentResponseSchema, AttachmentCreateSchema
from backend.app.service.attachment import AttachmentService, get_attachment_service


router = APIRouter(
    prefix="/attachment",
)


@router.get("/")
async def get_attachments():
    content = """
<body>
<form action="/attachment/" enctype="multipart/form-data" method="post">
<input name="file" type="file">
<input type="submit">
</form>
<form action="/attachment/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

# @router.post("/")
# async def get_attachments(
#     timeline_id: int,
#     event_id: int,
# ):
#     return


@router.post(
    "/",
    response_model=AttachmentResponseSchema,
    status_code=201,
)
async def create_attachment(
        # request_create_data: AttachmentCreateSchema,
        file: Annotated[UploadFile, File(description="A file read as UploadFile")],
        attachment_service: AttachmentService = Depends(get_attachment_service),
):
    # file_mimetype, _ = guess_type(file.filename)
    # storage_key =
    # attachment_data = {
    #     "mime_type": file_mimetype,
    #     "file_size": file.size,
    #     "storage_key":
    # }
    request_create_data = {
        "caption": "Some caption",
        "event_id": 1
    }
    attachment = await attachment_service.create_attachment(file, request_create_data)

    return attachment



@router.get(
    "/{attachment_id}",

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



