from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import and_, delete, exists, or_, select
from sqlalchemy.exc import IntegrityError

from backend.app.model import FriendRequest, Friends

from .base import BaseService
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

    async def retrieve_and_block_request(self, request_id: UUID, receiver_id: UUID):
        query = (
            select(self.model)
            .with_for_update()
            .where(
                self.model.id == request_id,
                self.model.receiver_id == receiver_id
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def accept_request(
        self,
        request_id: UUID,
        receiver_id: UUID,
        friend_service: FriendsService,
    ) -> Friends | None:
        try:
            async with self.session.begin():
                request = await self.retrieve_and_block_request(request_id, receiver_id)
                if request is None:
                    return None

                if await friend_service.check_existing_friendship(request.sender_id, request.receiver_id):
                    raise HTTPException(status_code=409, detail="Users are already friends")

                friendship = Friends(user_id=request.sender_id, friend_id=request.receiver_id)
                self.session.add(friendship)
                await self.session.delete(request)
        except IntegrityError as exc:
            if getattr(exc.orig, "sqlstate", None) == "23505":
                raise HTTPException(status_code=409, detail="Users are already friends") from exc
            raise

        return friendship

    async def reject_request(
            self,
            request_id: UUID,
            user_id: UUID
    ):
        async with self.session.begin():
            query = (
                delete(self.model)
                .where(
                    self.model.id == request_id,
                    or_(
                        self.model.sender_id == user_id,
                        self.model.receiver_id == user_id
                    )
                )
                .returning(self.model.id)
            )
            result = await self.session.execute(query)
            return result.scalar_one_or_none()
