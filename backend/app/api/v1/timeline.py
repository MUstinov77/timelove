from typing import Annotated

from fastapi import APIRouter, Depends


from backend.app.schema.timeline import TimelineCreateUpdateSchema, TimelineResponseSchema

router = APIRouter(
    prefix="/timeline",
)

@router.get(
    "/{timeline_id}",
    response_model=TimelineResponseSchema
)
async def get_timeline(
        timeline_id: int,
        timeline_service: Annotated[TimelineService, Depends(get_timeline_service)]
):
    timeline = ...
    return timeline

@router.get(
    "/",
    response_model=list[TimelineResponseSchema]
)
async def get_my_timelines(
    timeline_service: Annotated[TimelineService, Depends(get_timeline_service)]
):
    timelines = ...
    return timelines

@router.post(
    "/",
    response_model=TimelineResponseSchema,
)
async def create_timeline(
        create_data: TimelineCreateSchema,
        timeline_service: Annotated[TimelineService, Depends(get_timeline_service)]
):
    timeline = ...
    return timeline

@router.patch(
    "/{timeline_id}",
    response_model=TimelineResponseSchema
)
async def update_timeline(
        timeline_id: int,
        timeline_service: Annotated[TimelineService, Depends(get_timeline_service)]
):
    timeline = ...
    return timeline

@router.delete("/{timeline_id}")
async def delete_timeline(
        timeline_id: int,
        timeline_service: Annotated[TimelineService, Depends(get_timeline_service)]
):
    timeline = ...
    return timeline
