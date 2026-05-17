from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.app.core.auth.jwt import JWTService
from backend.app.core.exceptions import NotFoundException
from backend.app.core.utils.encrypt import get_hashed_password
from backend.app.model.user import User
from backend.app.schema.auth import Token, UserSignupSchema, UserLoginSchema
# from backend.app.service.auth.service import get_auth_service
from backend.app.service.user import UserService, get_user_service
from backend.app.core.utils.encrypt import verify_password

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
        login_data: OAuth2PasswordRequestForm = Depends(),
        user_service: UserService = Depends(get_user_service)
):
    user = await user_service.retrieve_one(User.email, login_data.username)
    if not user:
        raise NotFoundException
    if not await verify_password(login_data.password, user.hashed_password):
        raise NotFoundException
    token = JWTService().create_and_encode_token({
        "user_id": user.id,
        "username": user.email
    })
    return {"access_token": token}