import os
import os.path
import uuid
from mimetypes import guess_extension, guess_type

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.configuration import settings
from backend.app.core.datastore import postgres_session_provider
from backend.app.model.attachment import Attachment
from backend.app.service.base import BaseService


def get_attachment_service(
        session: AsyncSession = Depends(postgres_session_provider),
):
    return AttachmentService(session)


class AttachmentService(BaseService):

    model = Attachment

    async def create_attachment(self, file, request_data):
        mime_type, _ = guess_type(file.filename)

        file_id = uuid.uuid4()
        file_extension = guess_extension(mime_type)
        new_file_name = f"{file_id}{file_extension}"
        storage_key = os.path.join(settings.ATTACHMENTS_DIRECTORY_PATH, new_file_name)

        attachment_create_data = {
            "media_type": "image",
            "mime_type": mime_type,
            "storage_key": storage_key,
            "file_size": file.size,
            "sort_order": 0,
        }

        attachment_create_data.update(request_data)
        attachment = await self.create_instance(attachment_create_data)
        try:
            file_content = await file.read()
            with open(attachment.storage_key, "wb") as f:
                f.write(file_content)
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail="Attachment creation failed")
        return attachment

    async def delete_attachment(self, obj_id: int):
        attachment = await self.delete_instance(obj_id)
        if not attachment:
            raise HTTPException(status_code=404, detail="Attachment not found")
        try:
            os.remove(attachment.storage_key)
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail="Attachment deletion failed")
        return attachment