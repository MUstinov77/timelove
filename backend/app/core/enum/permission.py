from enum import StrEnum


class MemberPermission(StrEnum):
    DEFAULT = "DEFAULT"
    MODERATOR = "MODERATOR"
    ADMIN = "ADMIN"