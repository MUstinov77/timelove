from contextlib import asynccontextmanager

from backend.app.api.v1 import api_router
from backend.app.core.configuration import get_settings
from backend.app.core.datastore import destroy_db, init_db
from fastapi import FastAPI

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    try:
        yield
    finally:
        await destroy_db()

def create_app():
    app = FastAPI(
        title=settings.TITLE,
        lifespan=lifespan,
    )

    app.include_router(api_router)

    return app
