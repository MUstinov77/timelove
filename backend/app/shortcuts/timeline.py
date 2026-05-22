from fastapi import Depends

from backend.app.model.timeline import Timeline
from backend.app.service.timeline import get_timeline_service, TimelineService


async def retrieve_timeline(
        timeline_id: int,
        timeline_service: TimelineService = Depends(get_timeline_service),
):
    timeline = await timeline_service.retrieve_one(Timeline.id, timeline_id)
    return timeline