from pydantic import BaseModel

from datetime import date

class EventCreateUpdateSchema(BaseModel):
    title: str
    event_date: date
    description: str


class EventResponseSchema(BaseModel):
    id: int
    title: str
    event_date: date
    description: str