import uuid
from mimetypes import guess_type

import anyio
from fastapi import UploadFile

from backend.app.core.configuration import settings
from backend.app.core.exceptions import FileTooLargeException, UnsupportedMediaTypeException

CHUNK_SIZE = 1024 * 1024 # 1 Mb
MAX_FILE_SIZE = 200 * 1024 * 1024 # 200 Mb
ALLOWED_MIME_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "video/mp4": ".mp4",
    "audio/mpeg": ".mp3",
}


def get_attachment_path(storage_key: str) -> anyio.Path:
    return anyio.Path(settings.ATTACHMENTS_DIRECTORY_PATH) / storage_key


def prepare_attachment_create_data(file: UploadFile) -> tuple[dict, anyio.Path]:
    mime_type, _ = guess_type(file.filename)

    file_extension = ALLOWED_MIME_TYPES.get(mime_type)
    if file_extension is None:
        raise UnsupportedMediaTypeException
    if file.size is None or file.size > MAX_FILE_SIZE:
        raise FileTooLargeException

    storage_key = f"{uuid.uuid7()}{file_extension}"
    attachment_create_data = {
        "media_type": mime_type.split("/")[0],
        "mime_type": mime_type,
        "storage_key": storage_key,
        "file_size": file.size,
    }

    return attachment_create_data, get_attachment_path(storage_key)


async def write_attachment_chunked(file: UploadFile, file_path: anyio.Path) -> None:
    # async writing file to directory using thread by anyio lib
    try:
        async with await file_path.open("wb") as f:
            while chunk := await file.read(CHUNK_SIZE):
                await f.write(chunk)
    except BaseException:
        # also covers CancelledError when client drops the connection
        await file_path.unlink(missing_ok=True)
        raise
