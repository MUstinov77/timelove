from datetime import date

from pydantic import BaseModel


class EventCreateUpdateSchema(BaseModel):
    title: str
    event_date: date
    description: str

class EventUpdateSchema(BaseModel):
    title: str | None = None
    event_date: date | None = None
    description: str | None = None



class EventResponseSchema(BaseModel):
    id: int
    title: str
    event_date: date
    description: str
    # files: list[bytes]
