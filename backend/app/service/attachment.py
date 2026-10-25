import os
import os.path
import uuid
from mimetypes import guess_extension, guess_type

from fastapi import Depends, HTTPException, UploadFile
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.utils.attachment import prepare_attachment_create_data
from backend.app.core.configuration import settings
from backend.app.core.datastore import postgres_session_provider
from backend.app.model.attachment import Attachment
from backend.app.model.event import Event
from backend.app.schema.attachment import AttachmentCreateSchema
from backend.app.service.base import BaseService


def get_attachment_service(
        session: AsyncSession = Depends(postgres_session_provider),
):
    return AttachmentService(session)


class AttachmentService(BaseService):

    model = Attachment

    async def create_attachment(self, file: UploadFile, request_data):
        try:
            attachment_create_data = await prepare_attachment_create_data(file)

            attachment_create_data.update(request_data)
            attachment = Attachment(**attachment_create_data)
            self.session.add(attachment)
            file_content = await file.read()
            with open(attachment.storage_key, "wb") as f:
                f.write(file_content)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail="Attachment creation failed")
        return attachment


    async def delete_attachment(
            self,
            timeline_id: int,
            event_id: int,
            attachment_id: int,
    ):
        attachment = await self.retrieve_attachment(timeline_id, event_id, attachment_id)
        if not attachment:
            return None

        deleted = await self.delete(attachment_id)
        if not deleted:
            return None

        try:
            os.remove(attachment.storage_key)
            await self.session.commit()
        except Exception:
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
                Event.id == self.model.event_id
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
            join(
                Event,
                Event.id == self.model.event_id
            ).
            where(
                self.model.id == attachment_id,
                self.model.event_id == event_id,
                Event.timeline_id == timeline_id,
            )
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def update_attachment(
            self,
            timeline_id: int,
            event_id: int,
            attachment_id: int,
            updated_data: dict
    ):
        attachment = await self.retrieve_attachment(timeline_id, event_id, attachment_id)
        if not attachment:
            return None
        query = (
            update(self.model).
            where(
                self.model.id == attachment_id,
            ).
            values(**updated_data).
            returning(self.model)
        )
        result = await self.session.execute(query)
        await self.session.commit()
        return result.scalars().first()
