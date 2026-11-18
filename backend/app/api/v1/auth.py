from typing import Annotated

from fastapi import APIRouter, Form, status

from backend.app.core.auth.jwt import JWTService
from backend.app.core.exception.auth import LoginCredentialException
from backend.app.core.utils.encrypt import get_hashed_password, verify_password
from backend.app.dependencies.service import UserServiceDep
from backend.app.model.user import User
from backend.app.schema.auth import Token, UserLoginSchema, UserSignupSchema

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
        user_service: UserServiceDep
):
    user_data = create_data.model_dump(exclude={"password"})
    hashed_password = await get_hashed_password(create_data.password.get_secret_value())
    user_data["hashed_password"] = hashed_password
    await user_service.create(user_data)
    return {"message": "User created"}


@router.post(
    "/login",
    response_model=Token
)
async def login(
        login_data: Annotated[UserLoginSchema, Form()],
        user_service: UserServiceDep
):
    user = await user_service.retrieve_one(User.email, login_data.email)
    if not user:
        raise LoginCredentialException
    if not await verify_password(login_data.password.get_secret_value(), user.hashed_password):
        raise LoginCredentialException
    token = JWTService().create_and_encode_token({
        "user_id": user.id,
        "username": user.email
    })
    return {"access_token": token}
