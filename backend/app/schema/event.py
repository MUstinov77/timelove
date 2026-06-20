from datetime import date

from pydantic import BaseModel


class EventCreateUpdateSchema(BaseModel):
    title: str
    event_date: date
    description: str



class EventResponseSchema(BaseModel):
    id: int
    title: str
    event_date: date
    description: str
    # files: list[bytes]