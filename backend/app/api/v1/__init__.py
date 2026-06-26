from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException

from backend.app.service.attachment import AttachmentService, get_attachment_service
from backend.app.api.v1 import auth, event, timeline
from backend.app.schema.attachment import AttachmentResponseSchema

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(timeline.router)


@api_router.get("/")
async def health_check():
    return {"status": "ok"}

@api_router.get(
    "/attachment/{attachment_id}/file",
    response_model=AttachmentResponseSchema
)
async def get_attachment_file(
        attachment_id: int,
        attachment_service: AttachmentService = Depends(get_attachment_service),
):
    print("Here")
    attachment = await attachment_service.retrieve_one_by_id(attachment_id)
    if not attachment:
        raise HTTPException(status_code=401, detail="Attachment not found")
    return attachment

