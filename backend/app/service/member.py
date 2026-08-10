from typing import Any

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.datastore import postgres_session_provider
from backend.app.model.timeline_members import TimelineMembers

from .base import BaseService


async def get_member_service(
    session: AsyncSession = Depends(postgres_session_provider)
):
    return MemberService(session)


class MemberService(BaseService):

    model = TimelineMembers

    async def retrieve_member_permission(self, timeline_id: int, user_id: int):
        query = select(self.model.member_permission).where(
            self.model.timeline_id == timeline_id,
            self.model.member_id == user_id
        )
        result = await self.session.execute(query)
        return result.scalar()

    async def retrieve_one(self, field: Any, field_value: Any, user_id: int, *args, **kwargs):
        query = select(self.model).where(
            self.model.timeline_id == field_value,
            self.model.member_id == user_id
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def retrieve_membership(self, timeline_id: int, user_id: int):
        query = select(self.model).where(
            self.model.timeline_id == timeline_id,
            self.model.member_id == user_id
        )
        result = await self.session.execute(query)
        return result.scalars().first()
