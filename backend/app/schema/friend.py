from uuid import UUID

from pydantic import BaseModel

class FriendCreateSchema(BaseModel):
    user_id: UUID