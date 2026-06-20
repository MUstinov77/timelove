from backend.app.api.v1 import auth, event, timeline, attachment
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(timeline.router)
api_router.include_router(attachment.router)


@api_router.get("/")
async def health_check():
    return {"status": "ok"}
