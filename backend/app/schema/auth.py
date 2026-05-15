from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class UserSignupSchema(BaseModel):
    email: EmailStr
    password: str

    first_name: str | None
    last_name: str | None

    class Config:
        extra = "ignore"


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        extra = "ignore"
