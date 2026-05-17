from backend.app.core.enum.media import MediaType
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Media(Base):

    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(Enum(MediaType))