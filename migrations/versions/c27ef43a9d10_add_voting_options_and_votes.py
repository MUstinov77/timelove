"""Add voting options and votes."""

import sqlalchemy as sa
from alembic import op

revision = "c27ef43a9d10"
down_revision = "b8d6e037c4a1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "voting_options",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("voting_id", sa.Uuid(), nullable=False),
        sa.Column("text", sa.String(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["voting_id"], ["votings.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("voting_id", "id", name="uq_voting_options_voting_id_id"),
        sa.UniqueConstraint(
            "voting_id", "position", name="uq_voting_options_voting_id_position"
        ),
    )
    op.create_table(
        "votes",
        sa.Column("voting_id", sa.Uuid(), primary_key=True),
        sa.Column("voter_id", sa.Uuid(), primary_key=True),
        sa.Column("option_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.current_timestamp(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["voter_id"], ["users.id"]),
        sa.ForeignKeyConstraint(
            ["voting_id", "option_id"],
            ["voting_options.voting_id", "voting_options.id"],
            name="fk_votes_voting_option",
            ondelete="CASCADE",
        ),
    )
    op.create_index("ix_votes_voting_id_option_id", "votes", ["voting_id", "option_id"])


def downgrade() -> None:
    op.drop_table("votes")
    op.drop_table("voting_options")
