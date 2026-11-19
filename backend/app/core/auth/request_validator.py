from typing import Annotated

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from backend.app.core.auth.jwt import JWTService
from backend.app.schema.auth import AccessTokenPayload

auth_schema = OAuth2PasswordBearer(tokenUrl="auth/login")


async def authenticate_user(
        token: Annotated[str, Depends(auth_schema)],
):
    try:
        access_token_payload: AccessTokenPayload = JWTService().decode_access_token(token)
        user_id = access_token_payload.sub
        return user_id
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
