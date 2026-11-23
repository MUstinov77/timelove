from uuid import UUID

from fastapi import APIRouter, HTTPException

from backend.app.core.exceptions import NotFoundException
from backend.app.dependencies.auth import AuthUserDep
from backend.app.dependencies.service import (
    FriendRequestServiceDep,
    FriendsServiceDep,
    UserServiceDep,
)

router = APIRouter(
    prefix="/friends",
)

@router.get("/")
async def get_my_friends():
    pass

@router.post("/{receiver_id}")
async def send_friend_request(
        receiver_id: UUID,
        friend_request_service: FriendRequestServiceDep,
        friend_service: FriendsServiceDep,
        user_service: UserServiceDep,
        user_id: AuthUserDep
):
    friend_request = await friend_request_service.send_friend_request(user_id, receiver_id, friend_service, user_service)
    if not friend_request:
        raise HTTPException(
            400,
            "Fail to send friend request"
        )
    return {"message": "Friend request created"}


@router.delete("/")
async def delete_from_friends():
    pass


@router.post("/{request_id}/accept")
async def accept_friendship_request(
        request_id: UUID,
        friend_request_service: FriendRequestServiceDep,
        friend_service: FriendsServiceDep,
        user_id: AuthUserDep
):
    friendship = await friend_request_service.accept_request(
        request_id=request_id,
        receiver_id=user_id,
        friend_service=friend_service,
    )
    if friendship is None:
        raise NotFoundException()
    return {"message": "User added to friends"}



@router.post("/{request_i}/discard")
async def discard_friendship_request():
    pass
