from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.model.base import Base

if TYPE_CHECKING:
    from backend.app.model.event import Event


class Attachment(Base):

    __tablename__ = "attachments"

    id: Mapped[int] = mapped_column(primary_key=True)

    media_type: Mapped[str] = mapped_column(
        nullable=False,
    )
    mime_type: Mapped[str] = mapped_column(String(127), nullable=False)

    storage_key: Mapped[str] = mapped_column(String(512), nullable=False)
    thumbnail_key: Mapped[str | None] = mapped_column(String(512), nullable=True)

    file_size: Mapped[int] = mapped_column(BigInteger, nullable=False)

    width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    height: Mapped[int | None] = mapped_column(Integer, nullable=True)
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

    checksum_sha256: Mapped[str | None] = mapped_column(String(64), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    caption: Mapped[str | None] = mapped_column(Text, nullable=True)

    
    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    event: Mapped["Event"] = relationship(
        back_populates="attachments",
        lazy="raise",
    )