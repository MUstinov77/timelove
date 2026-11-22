from uuid import UUID

from sqlalchemy import select, exists, or_, and_
from .base import BaseService
from backend.app.model import FriendRequest
from .friends import FriendsService
from .user import UserService


class FriendRequestService(BaseService):

    model = FriendRequest

    async def send_friend_request(
            self,
            sender_id: UUID,
            receiver_id: UUID,
            friend_service: FriendsService,
            user_service: UserService
    ):
        if (
                not await user_service.check_user_exists(sender_id) or
                not await user_service.check_user_exists(receiver_id) or
                await friend_service.check_existing_friendship(sender_id, receiver_id) or
                await self.check_existing_request(sender_id, receiver_id)
        ):
            return None
        return await self.create({"sender_id": sender_id, "receiver_id": receiver_id})

    async def check_existing_request(self, sender_id: UUID, receiver_id: UUID):
        query = (
            select(
                exists(
                    select(1)
                    .where(
                        or_(
                            and_(
                                self.model.sender_id == sender_id,
                                self.model.receiver_id == receiver_id
                            ),
                            and_(
                                self.model.sender_id == receiver_id,
                                self.model.receiver_id == sender_id
                            )
                        )
                    )
                )
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one()

    async def apply_request(self, request_id: UUID, receiver_id: UUID):
        query = (
            select(self.model)
            .where(
                self.model.id == request_id,
                self.model.receiver_id == receiver_id
            )
            .with_for_update()
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
