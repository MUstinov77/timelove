from uuid import UUID

from sqlalchemy import select, exists, and_, or_

from backend.app.model import Friends

from .base import BaseService


class FriendsService(BaseService):

    model = Friends

    async def check_existing_friendship(self, sender_id: UUID, receiver_id: UUID):
        query = (
            select(
                exists(
                    select(1)
                    .where(
                        or_(
                            and_(
                                self.model.user_id == sender_id,
                                self.model.friend_id == receiver_id
                            ),
                            and_(
                                self.model.user_id == receiver_id,
                                self.model.friend_id == sender_id
                            )
                        )
                    )
                )
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one()