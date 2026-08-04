from fastapi import Depends
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.datastore import postgres_session_provider
from backend.app.model.timeline import Timeline
from backend.app.model.timeline_members import TimelineMembers

from .base import BaseService


def get_timeline_service(
        session: AsyncSession = Depends(postgres_session_provider)
):
    return TimelineService(session)


class TimelineService(BaseService):

    model = Timeline

    async def get_timelines_by_user_id(self, user_id: int):
        query = (
            select(self.model).
            join(
                TimelineMembers,
                TimelineMembers.member_id == user_id
            ).
            where(
                TimelineMembers.member_id == user_id
            )
        )
        result = await self.session.execute(query)
        return result.scalars().all()

