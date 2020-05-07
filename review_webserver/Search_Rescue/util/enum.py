from enum import Enum, unique


@unique
class JobTypeEnum(Enum):
    NULL = -1
    OIL = 0
    RESCUE = 1


@unique
class TaskStateEnum(Enum):
    '''
        对应的是 user_jobuserrate -> state 以及 user_taskinfo -> state

        # TODO:[*] 20-05-07 此处与枚举 users/models.py -> CHOICE_STATUS 相对应，此处如果处理使 enum -> 元祖
    '''
    RUNNING = 1
    COMPLETED = 2
    WAITTING = 3
    ERROR = 4
    UNUSED = 5

