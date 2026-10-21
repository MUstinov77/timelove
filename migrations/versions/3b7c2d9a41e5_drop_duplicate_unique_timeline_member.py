"""Drop duplicate unique constraint on timeline_members

Revision ID: 3b7c2d9a41e5
Revises: d0daa3f3a5af
Create Date: 2026-10-21 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '3b7c2d9a41e5'
down_revision: Union[str, Sequence[str], None] = 'd0daa3f3a5af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # duplicates the primary key (timeline_id, member_id)
    op.drop_constraint('unique_timeline_member', 'timeline_members', type_='unique')


def downgrade() -> None:
    """Downgrade schema."""
    op.create_unique_constraint(
        'unique_timeline_member', 'timeline_members', ['timeline_id', 'member_id']
    )
