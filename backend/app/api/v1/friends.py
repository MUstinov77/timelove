from uuid import UUID

from fastapi import APIRouter

from backend.app.schema.friend import FriendCreateSchema

router = APIRouter(
    prefix="/friends"
)

@router.get("/")
async def get_my_friends():
    pass

@router.post("/{user_id}")
async def add_user_to_friends(
        friend_create_data: FriendCreateSchema
):


@router.delete("/")
async def delete_from_friends():
    pass