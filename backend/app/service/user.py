from uuid import UUID

from sqlalchemy import exists, select

from backend.app.model import User

from .base import BaseService


class UserService(BaseService):

    model = User

    async def check_user_exists(self, user_id: UUID):
        query = (
            select(
                exists(
                    select(1)
                    .where(self.model.id == user_id)
                )
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one()

