from fastapi import APIRouter


router = APIRouter(
    prefix="/friends"
)

@router.get("/")
async def get_my_friends():
    pass

@router.post("/")
async def add_user_to_friends():
    pass

@router.delete("/")
async def delete_from_friends():
    pass