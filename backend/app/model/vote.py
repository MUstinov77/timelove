from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, ForeignKeyConstraint, Index, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Vote(Base):
    __tablename__ = "votes"
    __table_args__ = (
        ForeignKeyConstraint(
            ["voting_id", "option_id"],
            ["voting_options.voting_id", "voting_options.id"],
            name="fk_votes_voting_option",
            ondelete="CASCADE",
        ),
        Index("ix_votes_voting_id_option_id", "voting_id", "option_id"),
    )

    voting_id: Mapped[UUID] = mapped_column(primary_key=True)
    voter_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    option_id: Mapped[UUID]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.current_timestamp(),
    )
