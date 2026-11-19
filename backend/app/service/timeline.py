from uuid import UUID

from sqlalchemy import select

from backend.app.model.timeline import Timeline
from backend.app.model.timeline_members import TimelineMembers

from .base import BaseService


class TimelineService(BaseService):

    model = Timeline

    async def get_timelines_by_user_id(self, user_id: UUID):
        query = (
            select(self.model.id, self.model.title, TimelineMembers.member_permission).
            join(TimelineMembers).
            where(TimelineMembers.member_id == user_id)
        )
        result = await self.session.execute(query)
        return result.all()

    async def retrieve_timeline(self, obj_id: int, user_id: UUID):
        query = (
            select(self.model.id, self.model.title, TimelineMembers.member_permission).
            join(TimelineMembers).
            where(
                TimelineMembers.timeline_id == obj_id,
                TimelineMembers.member_id == user_id
            )
        )
        result = await self.session.execute(query)
        return result.one_or_none()

