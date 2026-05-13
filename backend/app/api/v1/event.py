from fastapi import APIRouter

from backend.app.schema.event import EventCreateUpdateSchema, EventResponseSchema

router = APIRouter(
    prefix="/event",
)

@router.get(
    "/{event_id}",
    response_model=EventResponseSchema,
)
async def get_event(
        event_id: int,
        event_service: Annotated[EventService, Depends(get_event_service)]
):
    event = ...
    return event

@router.get(
    "/",
    response_model=list[EventResponseSchema]
)
async def get_my_events(
        event_service: Annotated[EventService, Depends(get_event_service)]
):
    events = ...
    return events

@router.post(
    "/",
    response_model=EventResponseSchema,
)
async def create_event():
    event = ...
    return event

@router.patch(
    "/{event_id}",
    response_model=EventResponseSchema
)
async def update_event():
    event = ...
    return event

@router.delete("/{event_id}")
async def delete_event():
    event = ...
    ...
