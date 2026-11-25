"""Add friendships and friend requests."""

import sqlalchemy as sa
from alembic import op

revision = "98be498f65d3"
down_revision = "1737beee2e22"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "friends",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("friend_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["friend_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "friend_id"),
    )
    op.create_table(
        "friend_requests",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("sender_id", sa.Uuid(), nullable=False),
        sa.Column("receiver_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.current_timestamp(),
            nullable=False,
        ),
        sa.CheckConstraint("sender_id <> receiver_id", name="ck_friend_requests_different_users"),
        sa.ForeignKeyConstraint(["sender_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["receiver_id"], ["users.id"], ondelete="CASCADE"),
    )
    op.create_index(
        "uq_friend_requests_user_pair",
        "friend_requests",
        [sa.text("least(sender_id, receiver_id)"), sa.text("greatest(sender_id, receiver_id)")],
        unique=True,
    )


def downgrade() -> None:
    op.drop_table("friend_requests")
    op.drop_table("friends")
