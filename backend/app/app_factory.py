import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.middleware.errors import ServerErrorMiddleware

from backend.app.api.v1 import api_router
from backend.app.core.configuration import get_settings
from backend.app.core.datastore import destroy_db, init_db
from backend.app.core.exception.handlers import internal_server_error

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    try:
        os.mkdir(settings.ATTACHMENTS_DIRECTORY_PATH)
    except FileExistsError:
        print("Attachments directory already exists")

    try:
        yield
    finally:
        await destroy_db()

def create_app():
    app = FastAPI(
        title=settings.TITLE,
        lifespan=lifespan,
    )

    app.add_middleware(
        ServerErrorMiddleware,
        handler=internal_server_error
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


    app.include_router(api_router)

    return app
