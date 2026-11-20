from fastapi import APIRouter


router = APIRouter(
    prefix="/users",
)

@router.get("/{user_id}")
async def get_user_by_id():
    pass

@router.get("/")
async def get_users():
    pass
