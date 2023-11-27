from enum import Enum


class DocumentStatusEnum(Enum):
    NEW = 'new'
    PROCESS = 'process'
    COMPLETED = 'completed'
    SUCCESS = 'success'
    EXPIRED = 'expired'


class UsersPositionEnum(Enum):
    STUDENT = 1
    PROFESSOR = 2
    ADMINISTRATOR = 3
    LIBRARIAN = 4
    RESEARCHER = 5
    DEAN = 6
    CHAIRPERSON = 7
    JANITOR = 8


class ExpiringStatusEnum(Enum):
    OUTDATED = 'outdated'
    URGENT = 'urgent'
    XIMPORTANT = 'ximportant'
    IMPORTANT = 'important'
    FREELY = 'freely'
    XFREELY = 'xfreely'


EXPIRING_STATE_DIALECTS = {
    30: ExpiringStatusEnum.XFREELY,
    10: ExpiringStatusEnum.IMPORTANT,
    7: ExpiringStatusEnum.XIMPORTANT,
    1: ExpiringStatusEnum.URGENT,
    0: ExpiringStatusEnum.OUTDATED,
}

