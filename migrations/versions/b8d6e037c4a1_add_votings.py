"""Add votings."""

import sqlalchemy as sa
from alembic import op

revision = "b8d6e037c4a1"
down_revision = "49c51d97e621"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "votings",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("timeline_id", sa.Integer(), nullable=False),
        sa.Column("created_by_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.current_timestamp(),
            nullable=False,
        ),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["timeline_id"], ["timelines.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"]),
    )
    op.create_index("ix_votings_timeline_id", "votings", ["timeline_id"])


def downgrade() -> None:
    op.drop_table("votings")
