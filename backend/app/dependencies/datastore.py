from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.datastore import postgres_session_provider

PostgresSessionDep = Annotated[AsyncSession, Depends(postgres_session_provider)]
