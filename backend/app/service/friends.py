from .base import BaseService

from backend.app.model.friends import Friends


class FriendsService(BaseService):

    model = Friends