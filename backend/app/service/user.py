from backend.app.model.user import User

from .base import BaseService


class UserService(BaseService):

    model = User
