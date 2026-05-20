from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from backend.app.core.datastore import postgres_session_provider

from backend.app.core.enum.permission import MemberPermission
from backend.app.model.timeline_members import timeline_members
from .base import BaseService


async def get_member_service(
    session: AsyncSession = Depends(postgres_session_provider)
):
    return MemberService(session, timeline_members.c)


class MemberService(BaseService):

    async def is_admin(self, user_id: int, timeline_id: int):
        query = (
            select(self.model.member_permission).
            where(
            self.model.timeline_id == timeline_id,
                self.model.member_id == user_id
            )
        )
        result = await self.session.execute(query)
        return result.scalar() == MemberPermission.CHANGE

    async def retrieve_member_permission(self, timeline_id, user_id):
        query = select(self.model.member_permission).where(
            self.model.timeline_id == timeline_id,
            self.model.member_id == user_id
        )
        result = await self.session.execute(query)
        return result.scalar()