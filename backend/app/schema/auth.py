from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr

Password = Annotated[
    SecretStr,
    Field(
        min_length=10,
        max_length=20
    )
]


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserSignupSchema(BaseModel):
    email: EmailStr
    password: Password

    first_name: str | None = None
    last_name: str | None = None

    model_config = ConfigDict(extra="ignore")


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: Password

    model_config = ConfigDict(extra="ignore")
