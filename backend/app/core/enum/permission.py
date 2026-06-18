from enum import StrEnum


class MemberPermission(StrEnum):
    MEMBER = "MEMBER"
    MODERATOR = "MODERATOR"
    ADMIN = "ADMIN"