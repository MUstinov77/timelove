from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from backend.app.core.enum.permission import MemberPermission
from backend.app.model import Timeline, TimelineMembers

from .base import BaseService


class TimelineService(BaseService):

    model = Timeline

    async def create_timeline(self, title: str, user_id: UUID) -> Timeline:
        try:
            async with self.session.begin():
                timeline = Timeline(title=title)
                self.session.add(timeline)
                await self.session.flush()
                self.session.add(TimelineMembers(
                    timeline_id=timeline.id,
                    member_id=user_id,
                    member_permission=MemberPermission.ADMIN,
                ))
        except SQLAlchemyError as exc:
            raise HTTPException(400, "Error while creating instance") from exc
        return timeline

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

