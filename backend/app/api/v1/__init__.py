from fastapi import APIRouter

from backend.app.api.v1 import attachment, auth, event, timeline

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(timeline.router)


@api_router.get("/")
async def health_check():
    return {"status": "ok"}
