from typing import Annotated

from jwt.exceptions import ExpiredSignatureError, DecodeError, InvalidTokenError

from backend.app.core.auth.jwt import JWTService
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

auth_schema = OAuth2PasswordBearer(tokenUrl="auth/login")


async def authenticate_user(
        token: Annotated[str, Depends(auth_schema)],
):
    try:
        payload = JWTService().decode_token(token)
        user_dict = payload.get("context")
        return user_dict
    except (ExpiredSignatureError, DecodeError, InvalidTokenError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)