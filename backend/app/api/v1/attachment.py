from typing import Annotated

from fastapi import APIRouter, UploadFile, File, Request, Query
from fastapi.responses import HTMLResponse

from backend.app.schema.event import EventCreateUpdateSchema


router = APIRouter(
    prefix="/{event_id}/attachment",
)


# @router.get("/")
# async def get_attachments():
#     content = """
# <body>
# <form action="/attachment/files/" enctype="multipart/form-data" method="post">
# <input name="files" type="file">
# <input type="submit">
# </form>
# <form action="/attachment/uploadfiles/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# </body>
#     """
#     return HTMLResponse(content=content)

# @router.post("/")
# async def get_attachments(
#     timeline_id: int,
#     event_id: int,
# ):
#     return




@router.get(
    "/{attachment_id}",

)
async def get_attachment(
        attachment_id: int,
        attachment_service = ...
):
    return ...


