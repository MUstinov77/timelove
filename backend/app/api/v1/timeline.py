from fastapi import APIRouter

router = APIRouter(
    prefix="/timeline",
)

@router.get("/{timeline_id}")
async def get_timeline():
    ...

@router.get("/")
async def get_my_timelines():
    ...

@router.post("/")
async def create_timeline():
    ...

@router.patch("/{timeline_id}")
async def update_timeline():
    ...

@router.delete("/{timeline_id}")
async def delete_timeline():
    ...
