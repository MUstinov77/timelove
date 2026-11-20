from uuid import UUID

from fastapi import APIRouter

from backend.app.dependencies.service import FriendRequestServiceDep

router = APIRouter(
    prefix="/friends"
)

@router.get("/")
async def get_my_friends():
    pass

@router.post("/{user_id}")
async def add_user_to_friends(
        user_id: UUID,
        friend_request_service: FriendRequestServiceDep
):
    pass


@router.delete("/")
async def delete_from_friends():
    pass


@router.post("/{request_id}/apply")
async def apply_friendship_request():
    pass


@router.post("/{request_i}/discard")
async def discard_friendship_request():
    pass