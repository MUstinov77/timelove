from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class UserSignupLoginSchema(BaseModel):
    username: str
    password: str