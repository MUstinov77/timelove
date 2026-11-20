from backend.app.model import User

from .base import BaseService


class UserService(BaseService):

    model = User
