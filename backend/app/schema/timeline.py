from pydantic import BaseModel


class TimelineCreateUpdateSchema(BaseModel):

    title: str


class TimelineResponseSchema(BaseModel):
    id: int
    title: str
