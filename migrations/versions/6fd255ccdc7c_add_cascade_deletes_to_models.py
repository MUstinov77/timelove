"""Add cascade deletes to models

Revision ID: 6fd255ccdc7c
Revises: 17f8787d0e8d
Create Date: 2026-06-19 20:21:12.747410

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6fd255ccdc7c'
down_revision: Union[str, Sequence[str], None] = '17f8787d0e8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint('events_timeline_id_fkey', 'events', type_='foreignkey')
    op.create_foreign_key('events_timeline_id_fkey', 'events', 'timelines', ['timeline_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('timeline_members_timeline_id_fkey', 'timeline_members', type_='foreignkey')
    op.drop_constraint('timeline_members_member_id_fkey', 'timeline_members', type_='foreignkey')
    op.create_foreign_key('timeline_members_timeline_id_fkey', 'timeline_members', 'timelines', ['timeline_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('timeline_members_member_id_fkey', 'timeline_members', 'users', ['member_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('timeline_members_member_id_fkey', 'timeline_members', type_='foreignkey')
    op.drop_constraint('timeline_members_timeline_id_fkey', 'timeline_members', type_='foreignkey')
    op.create_foreign_key('timeline_members_member_id_fkey', 'timeline_members', 'users', ['member_id'], ['id'])
    op.create_foreign_key('timeline_members_timeline_id_fkey', 'timeline_members', 'timelines', ['timeline_id'], ['id'])
    op.drop_constraint('events_timeline_id_fkey', 'events', type_='foreignkey')
    op.create_foreign_key('events_timeline_id_fkey', 'events', 'timelines', ['timeline_id'], ['id'])
