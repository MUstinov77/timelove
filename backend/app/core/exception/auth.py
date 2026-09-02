from fastapi import status
from fastapi.exceptions import HTTPException

class WrongEmailException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong email or username"
        )

class WrongPasswordException(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong password"
        )
