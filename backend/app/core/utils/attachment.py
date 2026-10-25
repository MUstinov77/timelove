import uuid
from anyio import open_file, Path
from mimetypes import guess_type
from pathlib import Path

from fastapi import UploadFile

from backend.app.core.configuration import get_settings

settings = get_settings()

CHUNK_SIZE = 1024 * 1024 # 1 Mb
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


async def write_attachment_chunked(file: UploadFile, file_path: Path):
    # async writing file to directory using thread by anyio lib
    try:
        async with await open_file(file_path, "wb") as f:
            while chunk := await file.read(CHUNK_SIZE):
                await f.write(chunk)
    except Exception:
        await Path(file_path).unlink(missing_ok=True)

