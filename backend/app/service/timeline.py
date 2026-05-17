from backend.app.core.datastore import postgres_session_provider
from backend.app.model.timeline import Timeline
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseService


def get_timeline_service(
        session: AsyncSession = Depends(postgres_session_provider)
):
    return TimelineService(session, Timeline)


class TimelineService(BaseService):
    pass