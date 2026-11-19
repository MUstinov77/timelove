"""PostgreSQL migration checks in a temporary, rolled-back schema.

Run with TIMELOVE_TEST_POSTGRES=1 to enable database access.
"""

import importlib
import os
import unittest
from uuid import UUID, uuid4

import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine

from backend.app.core.configuration import settings
from backend.app.model.user import User

migration = importlib.import_module(
    "migrations.versions.1737beee2e22_convert_user_ids_to_uuid"
)


@unittest.skipUnless(
    os.environ.get("TIMELOVE_TEST_POSTGRES") == "1",
    "Set TIMELOVE_TEST_POSTGRES=1 to run PostgreSQL migration checks",
)
class UserUUIDMigrationTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.engine = create_async_engine(settings.DB_URI)
        self.addAsyncCleanup(self.engine.dispose)
        self.connection = await self.engine.connect()
        self.addAsyncCleanup(self.connection.close)
        transaction = await self.connection.begin()
        self.addAsyncCleanup(transaction.rollback)

        schema = f"test_user_uuid_{uuid4().hex}"
        await self.connection.execute(sa.text(f'CREATE SCHEMA "{schema}"'))
        await self.connection.execute(sa.text(f'SET LOCAL search_path TO "{schema}"'))
        for statement in (
            """CREATE TABLE users (
                id serial PRIMARY KEY,
                email varchar NOT NULL UNIQUE,
                hashed_password varchar NOT NULL,
                first_name varchar,
                last_name varchar
            )""",
            "CREATE TABLE timelines (id integer PRIMARY KEY, title varchar NOT NULL)",
            """CREATE TABLE timeline_members (
                timeline_id integer NOT NULL REFERENCES timelines(id) ON DELETE CASCADE,
                member_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                member_permission varchar NOT NULL,
                PRIMARY KEY (timeline_id, member_id)
            )""",
        ):
            await self.connection.execute(sa.text(statement))

    async def _migrate(self, operation):
        def run(connection):
            with Operations.context(MigrationContext.configure(connection)):
                operation()

        await self.connection.run_sync(run)

    async def _snapshot(self):
        users = await self.connection.execute(sa.text("""
            SELECT email, hashed_password, first_name, last_name
            FROM users ORDER BY email
        """))
        members = await self.connection.execute(sa.text("""
            SELECT users.email, membership.timeline_id, membership.member_permission
            FROM timeline_members AS membership
            JOIN users ON users.id = membership.member_id
            ORDER BY users.email, membership.timeline_id
        """))
        return users.all(), members.all()

    async def test_preserves_users_links_and_supports_new_users(self):
        await self.connection.execute(sa.text("""
            INSERT INTO users (id, email, hashed_password, first_name)
            VALUES (7, 'first@example.com', 'first-test-hash', 'First'),
                   (42, 'second@example.com', 'second-test-hash', 'Second')
        """))
        await self.connection.execute(sa.text("""
            INSERT INTO timelines (id, title) VALUES (1, 'First trip'), (2, 'Second trip')
        """))
        await self.connection.execute(sa.text("""
            INSERT INTO timeline_members (timeline_id, member_id, member_permission)
            VALUES (1, 7, 'ADMIN'), (2, 7, 'MEMBER'), (1, 42, 'MODERATOR')
        """))
        original = await self._snapshot()

        await self._migrate(migration.upgrade)
        self.assertEqual(await self._snapshot(), original)
        ids = (await self.connection.execute(sa.text("SELECT id FROM users"))).scalars()
        self.assertTrue(all(isinstance(value, UUID) and value.version == 7 for value in ids))

        new_id = (await self.connection.execute(
            User.__table__.insert().values(
                email="new@example.com", hashed_password="new-test-hash",
            ).returning(User.id)
        )).scalar_one()
        self.assertIsInstance(new_id, UUID)
        self.assertEqual(new_id.version, 7)
        await self.connection.execute(sa.text("""
            INSERT INTO timeline_members (timeline_id, member_id, member_permission)
            VALUES (2, :user_id, 'MEMBER')
        """), {"user_id": new_id})

        with self.assertRaises(IntegrityError):
            async with self.connection.begin_nested():
                await self.connection.execute(sa.text("""
                    INSERT INTO timeline_members (timeline_id, member_id, member_permission)
                    VALUES (2, :user_id, 'MEMBER')
                """), {"user_id": uuid4()})

        before_downgrade = await self._snapshot()
        await self._migrate(migration.downgrade)
        self.assertEqual(await self._snapshot(), before_downgrade)
        previous_max = (await self.connection.execute(
            sa.text("SELECT max(id) FROM users")
        )).scalar_one()
        next_id = (await self.connection.execute(sa.text("""
            INSERT INTO users (email, hashed_password)
            VALUES ('after-downgrade@example.com', 'test-hash') RETURNING id
        """))).scalar_one()
        self.assertEqual(next_id, previous_max + 1)

        await self.connection.execute(
            sa.text("DELETE FROM users WHERE email = 'new@example.com'")
        )
        remaining_members = (await self.connection.execute(
            sa.text("SELECT count(*) FROM timeline_members")
        )).scalar_one()
        self.assertEqual(remaining_members, 3)

    async def test_empty_tables_and_repeated_upgrade(self):
        await self._migrate(migration.upgrade)
        self.assertEqual(await self._snapshot(), ([], []))
        await self._migrate(migration.downgrade)
        first_id = (await self.connection.execute(sa.text("""
            INSERT INTO users (email, hashed_password)
            VALUES ('empty@example.com', 'test-hash') RETURNING id
        """))).scalar_one()
        self.assertEqual(first_id, 1)
        await self._migrate(migration.upgrade)
        migrated_id = (await self.connection.execute(sa.text("SELECT id FROM users"))).scalar_one()
        self.assertIsInstance(migrated_id, UUID)
        self.assertEqual(migrated_id.version, 7)

    async def test_missing_membership_pk_and_custom_user_pk(self):
        await self.connection.execute(sa.text(
            "ALTER TABLE timeline_members DROP CONSTRAINT timeline_members_pkey"
        ))
        await self.connection.execute(sa.text(
            "ALTER TABLE users RENAME CONSTRAINT users_pkey TO custom_user_key"
        ))
        await self.connection.execute(sa.text("""
            INSERT INTO users (id, email, hashed_password)
            VALUES (7, 'existing@example.com', 'test-hash')
        """))
        original = await self._snapshot()
        await self._migrate(migration.upgrade)
        self.assertEqual(await self._snapshot(), original)

        def primary_keys(connection):
            inspector = sa.inspect(connection)
            return (
                inspector.get_pk_constraint('users')['constrained_columns'],
                inspector.get_pk_constraint('timeline_members')['constrained_columns'],
            )

        self.assertEqual(
            await self.connection.run_sync(primary_keys),
            (['id'], ['timeline_id', 'member_id']),
        )
