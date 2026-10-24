import uuid
from mimetypes import guess_type
from pathlib import Path

from fastapi import UploadFile

from backend.app.schema.attachment import AttachmentCreateSchema
from backend.app.core.configuration import get_settings

settings = get_settings()

ALLOWED_MIME_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "video/mp4": ".mp4",
    "audio/mpeg": ".mp3",
}

async def prepare_attachment_create_data(file: UploadFile):
    mime_type, _ = guess_type(file.filename)

    file_extension = ALLOWED_MIME_TYPES.get(mime_type)
    if file_extension is None:
        raise Exception

    storage_key = f"{uuid.uuid7()}{file_extension}"
    file_path = Path(settings.ATTACHMENTS_DIRECTORY_PATH) / storage_key
    media_type = mime_type.split("/")[0]

    attachment_create_data = {
            "media_type": media_type,
            "mime_type": mime_type,
            "storage_key": file_path,
            "file_size": file.size,
        }

    return attachment_create_data


async def read_attachment_chunked():
    pass