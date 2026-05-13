from fastapi import APIRouter

from backend.app.api.v1 import timeline
from backend.app.api.v1 import event

api_router = APIRouter()

api_router.include_router(timeline.router)
api_router.include_router(event.router)

@api_router.get("/")
async def health_check():
    return {"status": "ok"}