"""Relative attachment storage_key

Revision ID: 7c41e9b2d5a3
Revises: 1985a8f75027
Create Date: 2026-10-25 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from backend.app.core.configuration import settings


# revision identifiers, used by Alembic.
revision: str = '7c41e9b2d5a3'
down_revision: Union[str, Sequence[str], None] = '1985a8f75027'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # keep only file name: absolute path -> "<uuid>.<ext>"
    op.execute(
        "UPDATE attachments "
        "SET storage_key = regexp_replace(storage_key, '^.*/', '') "
        "WHERE storage_key LIKE '%/%'"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        sa.text(
            "UPDATE attachments "
            "SET storage_key = :directory || storage_key "
            "WHERE storage_key NOT LIKE '%/%'"
        ).bindparams(directory=settings.ATTACHMENTS_DIRECTORY_PATH)
    )
