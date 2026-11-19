"""convert user ids to uuid

Revision ID: 1737beee2e22
Revises: 0ec254d00fb0
Create Date: 2026-11-19 12:59:05.455682

"""
from collections.abc import Sequence
from uuid import uuid7

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '1737beee2e22'
down_revision: str | Sequence[str] | None = '0ec254d00fb0'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Assign UUIDs to existing users and preserve their memberships."""
    _lock_tables()
    op.add_column('users', sa.Column('_uuid_id', sa.Uuid(), nullable=True))
    op.add_column(
        'timeline_members',
        sa.Column('_uuid_member_id', sa.Uuid(), nullable=True),
    )

    users = sa.table(
        'users',
        sa.column('id', sa.Integer()),
        sa.column('_uuid_id', sa.Uuid()),
    )
    connection = op.get_bind()
    rows = connection.execute(sa.select(users.c.id).order_by(users.c.id))
    update_user = (
        users.update()
        .where(users.c.id == sa.bindparam('old_id'))
        .values(_uuid_id=sa.bindparam('new_id'))
    )
    for batch in rows.partitions(1000):
        connection.execute(
            update_user,
            [{'old_id': row.id, 'new_id': uuid7()} for row in batch],
        )

    op.execute(sa.text('''
        UPDATE timeline_members AS membership
        SET _uuid_member_id = users._uuid_id
        FROM users
        WHERE membership.member_id = users.id
    '''))
    _replace_keys('_uuid_id', '_uuid_member_id', sa.Uuid())


def downgrade() -> None:
    """Restore integer keys and links, assigning fresh sequential IDs.

    Original integer IDs cannot be recovered from the generated UUIDs.
    Users created after the upgrade are preserved as well.
    """
    _lock_tables()
    op.add_column('users', sa.Column('_int_id', sa.Integer(), nullable=True))
    op.add_column(
        'timeline_members',
        sa.Column('_int_member_id', sa.Integer(), nullable=True),
    )
    op.execute(sa.text('''
        UPDATE users
        SET _int_id = numbered.new_id
        FROM (
            SELECT id, row_number() OVER (ORDER BY id)::integer AS new_id
            FROM users
        ) AS numbered
        WHERE users.id = numbered.id
    '''))
    op.execute(sa.text('''
        UPDATE timeline_members AS membership
        SET _int_member_id = users._int_id
        FROM users
        WHERE membership.member_id = users.id
    '''))
    _replace_keys('_int_id', '_int_member_id', sa.Integer())

    op.execute(sa.text('CREATE SEQUENCE users_id_seq AS integer OWNED BY users.id'))
    op.alter_column(
        'users', 'id', server_default=sa.text("nextval('users_id_seq'::regclass)"),
    )
    op.execute(sa.text('''
        SELECT setval(
            'users_id_seq', COALESCE(MAX(id), 1), MAX(id) IS NOT NULL
        )
        FROM users
    '''))


def _lock_tables() -> None:
    # Bound lock waiting; all DDL and data changes share Alembic's transaction.
    op.execute(sa.text("SET LOCAL lock_timeout = '5s'"))
    op.execute(sa.text('LOCK TABLE users, timeline_members IN ACCESS EXCLUSIVE MODE'))


def _replace_keys(user_column: str, member_column: str, key_type: sa.types.TypeEngine) -> None:
    inspector = sa.inspect(op.get_bind())
    user_pk = inspector.get_pk_constraint('users')['name']
    member_pk = inspector.get_pk_constraint('timeline_members')['name']
    op.drop_constraint(
        'timeline_members_member_id_fkey', 'timeline_members', type_='foreignkey',
    )
    if member_pk is not None:
        op.drop_constraint(member_pk, 'timeline_members', type_='primary')
    if user_pk is not None:
        op.drop_constraint(user_pk, 'users', type_='primary')

    op.drop_column('timeline_members', 'member_id')
    op.drop_column('users', 'id')
    op.alter_column(
        'users', user_column, new_column_name='id',
        existing_type=key_type, nullable=False,
    )
    op.alter_column(
        'timeline_members', member_column, new_column_name='member_id',
        existing_type=key_type, nullable=False,
    )

    op.create_primary_key('users_pkey', 'users', ['id'])
    op.create_primary_key(
        'timeline_members_pkey', 'timeline_members', ['timeline_id', 'member_id'],
    )
    op.create_foreign_key(
        'timeline_members_member_id_fkey', 'timeline_members', 'users',
        ['member_id'], ['id'], ondelete='CASCADE',
    )
