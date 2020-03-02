from enum import Enum, unique


@unique
class JobTypeEnum(Enum):
    NULL = -1
    OIL = 0
    RESCUE = 1
