from uuid import UUID

from pydantic import BaseModel

class FriendCreateSchema(BaseModel):
    user_id: UUID


class FriendSummary(BaseModel):
    id: UUID
    first_name: str | None
    last_name: str | None