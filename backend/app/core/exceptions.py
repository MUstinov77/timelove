from fastapi import status
from fastapi.exceptions import HTTPException


class NotFoundException(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )

class PermissionException(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

class UnsupportedMediaTypeException(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type"
        )

class FileTooLargeException(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail="File is too large"
        )
