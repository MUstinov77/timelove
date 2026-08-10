import os
import os.path
import uuid
from mimetypes import guess_extension, guess_type

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.configuration import settings
from backend.app.core.datastore import postgres_session_provider
from backend.app.model.attachment import Attachment
from backend.app.model.event import Event
from backend.app.model.timeline import Timeline
from backend.app.service.base import BaseService


def get_attachment_service(
        session: AsyncSession = Depends(postgres_session_provider),
):
    return AttachmentService(session)


class AttachmentService(BaseService):

    model = Attachment

    async def create_attachment(self, file, request_data):
        try:
            mime_type, _ = guess_type(file.filename)

            file_id = uuid.uuid4()
            file_extension = guess_extension(mime_type)
            media_type = mime_type.split("/")[0]
            new_file_name = f"{file_id}{file_extension}"
            storage_key = os.path.join(settings.ATTACHMENTS_DIRECTORY_PATH, new_file_name)

            attachment_create_data = {
                "media_type": media_type,
                "mime_type": mime_type,
                "storage_key": storage_key,
                "file_size": file.size,
            }

            attachment_create_data.update(request_data)
            attachment = await self.create(attachment_create_data)
            file_content = await file.read()
            with open(attachment.storage_key, "wb") as f:
                f.write(file_content)
        except Exception:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail="Attachment creation failed")
        return attachment

    async def delete_attachment(self, obj_id: int):
        attachment = await self.delete(obj_id)
        try:
            os.remove(attachment.storage_key)
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail="Attachment deletion failed")
        return attachment

    async def retrieve_event_attachments(
            self,
            timeline_id: int,
            event_id: int,
    ):
        query = (
            select(self.model).
            join(
                Event,
                Event.id == event_id,
            ).
            where(
                Event.timeline_id == timeline_id,
                self.model.event_id == event_id,
            )
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def retrieve_attachment(
            self,
            timeline_id: int,
            event_id: int,
            attachment_id: int,
    ):
        query = (
            select(self.model).
            join(Event).
            where(
                self.model.id == attachment_id,
                self.model.event_id == event_id,
                Event.timeline_id == timeline_id,
            )
        )
        result = await self.session.execute(query)
        return result.scalars().first()