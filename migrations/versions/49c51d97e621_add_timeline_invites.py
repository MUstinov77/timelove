"""Add timeline invites."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "49c51d97e621"
down_revision = "98be498f65d3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    permission_enum = postgresql.ENUM(
        "MEMBER", "MODERATOR", "ADMIN", name="member_permission_enum", create_type=False
    )
    op.create_table(
        "timeline_invites",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("timeline_id", sa.Integer(), nullable=False),
        sa.Column("sender_id", sa.Uuid(), nullable=False),
        sa.Column("receiver_id", sa.Uuid(), nullable=False),
        sa.Column("member_permission", permission_enum, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.current_timestamp(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["timeline_id"], ["timelines.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["sender_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["receiver_id"], ["users.id"], ondelete="CASCADE"),
        sa.CheckConstraint("sender_id <> receiver_id", name="ck_timeline_invites_different_users"),
        sa.UniqueConstraint("timeline_id", "receiver_id", name="uq_timeline_invites_recipient"),
    )
    op.create_index("ix_timeline_invites_receiver_id", "timeline_invites", ["receiver_id"])


def downgrade() -> None:
    op.drop_table("timeline_invites")
