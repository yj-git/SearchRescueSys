from enum import Enum, unique


@unique
class JobTypeEnum(Enum):
    NULL = -1
    OIL = 0
    RESCUE = 1


@unique
class TaskStateEnum(Enum):
    RUNNING = 1
    COMPLETED = 2
    WAITTING = 3
    ERROR = 4
    UNUSED = 5

