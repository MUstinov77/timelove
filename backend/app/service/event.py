from sqlalchemy import select

from backend.app.model.event import Event

from .base import BaseService


class EventService(BaseService):

    model = Event

    async def retrieve_event(
            self,
            timeline_id: int,
            event_id: int
    ):
        query = (
            select(self.model).
            where(
                self.model.id == event_id,
                self.model.timeline_id == timeline_id
            )
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def retrieve_timeline_events(
            self,
            timeline_id: int,
    ):
        query = (
            select(self.model).
            where(
                self.model.timeline_id == timeline_id
            )
        )
        result = await self.session.execute(query)
        return result.scalars().all()
