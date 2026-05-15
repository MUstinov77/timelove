from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.app.core.auth.jwt import JWTService
from backend.app.core.utils.encrypt import get_hashed_password
from backend.app.model.user import User
from backend.app.schema.auth import Token, UserSignupSchema
# from backend.app.service.auth.service import get_auth_service
from backend.app.service.user import UserService, get_user_service

BASE_PREFIX = "/auth"

router = APIRouter(
    prefix=BASE_PREFIX,
    tags=["auth"],
)


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED
)
async def signup(
        create_data: UserSignupSchema,
        user_service: UserService = Depends(get_user_service)
):
    user_data = create_data.model_dump()
    hashed_password = await get_hashed_password(user_data.pop("password"))
    user_data["hashed_password"] = hashed_password
    await user_service.create_instance(user_data)
    return {"message": "User created"}


@router.post(
    "/login",
    response_model=Token | None
)
async def login(
        login_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_service: UserService = Depends(get_user_service)
):
    print(login_data.username, login_data.password)
    return {"access_token": "", "token_type": "bearer"}
