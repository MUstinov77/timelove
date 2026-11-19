from typing import Annotated
from uuid import UUID

from fastapi import Depends

from backend.app.core.auth.request_validator import authenticate_user

AuthUserDep = Annotated[UUID, Depends(authenticate_user)]
