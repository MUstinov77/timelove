from typing import Annotated

from pydantic import BaseModel
from fastapi import Form

from backend.app.core.enum.attachment import AttachmentType


class AttachmentCreateSchema(BaseModel):
    caption: str | None

    @classmethod
    def as_form(
            cls,
            caption: Annotated[str | None, Form(None)]
    ):
        return cls(
            caption=caption
        )


class AttachmentResponseSchema(BaseModel):
    id: int
    media_type: AttachmentType
    mime_type: str
    storage_key: str
    thumbnail_key: str | None
    file_size: int
    width: int | None
    height: int | None
    duration_ms: int | None
    sort_order: int
    caption: str | None
    event_id: int

    # model_config = ConfigDict(from_attributes=True)
