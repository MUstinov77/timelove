from typing import Annotated

from fastapi import Depends

from backend.app.dependencies.datastore import PostgresSessionDep
from backend.app.service.attachment import AttachmentService
from backend.app.service.event import EventService
from backend.app.service.friends import FriendsService
from backend.app.service.member import MemberService
from backend.app.service.timeline import TimelineService
from backend.app.service.user import UserService


def get_attachment_service(
    session: PostgresSessionDep,
) -> AttachmentService:
    return AttachmentService(session)


def get_event_service(
    session: PostgresSessionDep,
) -> EventService:
    return EventService(session)


async def get_member_service(
    session: PostgresSessionDep,
) -> MemberService:
    return MemberService(session)


def get_timeline_service(
    session: PostgresSessionDep,
) -> TimelineService:
    return TimelineService(session)


def get_user_service(
    session: PostgresSessionDep,
) -> UserService:
    return UserService(session)


def get_friends_service(
        session: PostgresSessionDep,
) -> FriendsService:
    return FriendsService(session)


AttachmentServiceDep = Annotated[AttachmentService, Depends(get_attachment_service)]
EventServiceDep = Annotated[EventService, Depends(get_event_service)]
FriendsServiceDep = Annotated[FriendsService, Depends(get_friends_service)]
MemberServiceDep = Annotated[MemberService, Depends(get_member_service)]
TimelineServiceDep = Annotated[TimelineService, Depends(get_timeline_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
