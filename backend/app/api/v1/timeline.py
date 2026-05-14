from typing import Annotated

from fastapi import APIRouter, Depends

from backend.app.schema.timeline import TimelineCreateUpdateSchema, TimelineResponseSchema
from backend.app.service.timeline import TimelineService, get_timeline_service
from backend.app.model.timeline import Timeline

router = APIRouter(
    prefix="/timeline",
)

@router.get(
    "/{timeline_id}",
    response_model=TimelineResponseSchema
)
async def get_timeline(
    timeline_id: int,
    timeline_service: TimelineService = Depends(get_timeline_service)
):
    timeline = await timeline_service.retrieve_one(Timeline.id, timeline_id)
    if not timeline:
        raise ...
    return timeline

@router.get(
    "/",
    response_model=list[TimelineResponseSchema]
)
async def get_my_timelines(
    timeline_service: TimelineService = Depends(get_timeline_service)
):
    timelines = await timeline_service.retrieve_all()
    if not timelines:
        raise ...
    return timelines

@router.post(
    "/",
    response_model=TimelineResponseSchema,
)
async def create_timeline(
    create_data: TimelineCreateUpdateSchema,
    timeline_service: Annotated[TimelineService, Depends(get_timeline_service)]
):
    timeline = await timeline_service.create_instance(create_data.model_dump())
    if not timeline:
        raise ...
    return timeline

@router.patch(
    "/{timeline_id}",
    response_model=TimelineResponseSchema
)
async def update_timeline(
    timeline_id: int,
    update_data: TimelineCreateUpdateSchema,
    timeline_service: TimelineService = Depends(get_timeline_service)
):
    timeline = await timeline_service.update_instance(update_data.model_dump(), timeline_id)
    if not timeline:
        raise ...
    return timeline

@router.delete("/{timeline_id}")
async def delete_timeline(
    timeline_id: int,
    timeline_service: TimelineService = Depends(get_timeline_service)
):
    timeline = await timeline_service.delete_instance(timeline_id)
    if not timeline:
        raise ...
    return timeline
