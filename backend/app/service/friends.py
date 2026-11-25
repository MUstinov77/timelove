from uuid import UUID

from sqlalchemy import select, exists, and_, or_, union

from backend.app.model import Friends, User

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

    async def retrieve_user_friends(
            self,
            user_id: UUID
    ):
        friends_ids_cte = union(
            select(self.model.user_id.label("id"))
            .where(self.model.friend_id == user_id),
            select(self.model.friend_id.label("id"))
            .where(self.model.user_id == user_id)
        ).cte("friends_ids")
        query = (
            select(User.id, User.first_name, User.last_name)
            .where(User.id.in_(select(friends_ids_cte.c.id)))
        )
        result = await self.session.execute(query)
        return result.all()