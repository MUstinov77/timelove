from fastapi import APIRouter

router = APIRouter(
    prefix="/event",
)

@router.get("/{event_id}")
async def get_event():
    ...

@router.get("/")
async def get_my_events():
    ...

@router.post("/")
async def create_event():
    ...

@router.patch("/{event_id}")
async def update_event():
    ...

@router.delete("/{event_id}")
async def delete_event():
    ...
