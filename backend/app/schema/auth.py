from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr, field_validator

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

    @field_validator("password")
    @classmethod
    def reject_whitespace_only_password(cls, value: SecretStr):
        if not value.get_secret_value().strip():
            raise ValueError("Password cant contain only whitespaces")
        return value

    model_config = ConfigDict(extra="ignore")


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(alias="username")
    password: SecretStr

    model_config = ConfigDict(
        extra="ignore",
        validate_by_name=True
    )
