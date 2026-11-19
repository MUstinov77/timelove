from uuid import UUID

from sqlalchemy import select

from backend.app.model.timeline_members import TimelineMembers

from .base import BaseService


class MemberService(BaseService):

    model = TimelineMembers

    # async def retrieve_member_permission(self, timeline_id: int, user_id: int):
    #     query = select(self.model.member_permission).where(
    #         self.model.timeline_id == timeline_id,
    #         self.model.member_id == user_id
    #     )
    #     result = await self.session.execute(query)
    #     return result.scalar()

    # async def retrieve_one(self, field: Any, field_value: Any, user_id: int, *args, **kwargs):
    #     query = select(self.model).where(
    #         self.model.timeline_id == field_value,
    #         self.model.member_id == user_id
    #     )
    #     result = await self.session.execute(query)
    #     return result.scalars().first()

    async def retrieve_membership(self, timeline_id: int, user_id: UUID):
        query = select(self.model.member_permission).where(
            self.model.timeline_id == timeline_id,
            self.model.member_id == user_id
        )
        result = await self.session.execute(query)
        return result.scalars().first()
