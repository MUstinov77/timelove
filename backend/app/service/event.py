from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.datastore import postgres_session_provider
from backend.app.model.event import Event
from .base import BaseService


def get_event_service(
        session: AsyncSession = Depends(postgres_session_provider)
):
    return EventService(session, Event)


class EventService(BaseService):
    pass