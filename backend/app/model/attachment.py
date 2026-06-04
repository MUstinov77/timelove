from typing import TYPE_CHECKING
from backend.app.core.enum.attachment import AttachmentType
from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.model.base import Base


if TYPE_CHECKING:
    from backend.app.model.event import Event


class Attachment(Base):

    __tablename__ = "attachments"

    id: Mapped[int] = mapped_column(primary_key=True)
    mime_type: Mapped[str] = mapped_column(
        Enum(AttachmentType),
        nullable=False,
    )
    file_path: Mapped[str] = mapped_column(
        String(),
        nullable=False,
    )

    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    event: Mapped["Event"] = relationship(
        back_populates="attachments",
        lazy="selectin"
    )