from uuid import UUID, uuid7

from sqlalchemy import ForeignKey, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class VotingOption(Base):
    __tablename__ = "voting_options"
    __table_args__ = (
        UniqueConstraint("voting_id", "id", name="uq_voting_options_voting_id_id"),
        UniqueConstraint(
            "voting_id", "position", name="uq_voting_options_voting_id_position"
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True, default=uuid7)
    voting_id: Mapped[UUID] = mapped_column(
        ForeignKey("votings.id", ondelete="CASCADE")
    )
    text: Mapped[str] = mapped_column(String())
    position: Mapped[int]
