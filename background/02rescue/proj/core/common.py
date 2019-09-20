from enum import Enum
import time


class DataType(Enum):
    '''
        读取的搜救或溢油 data
    '''

    # 搜救
    Search_Rescue = 1
    # 溢油
    Oil_Spilling = 2


def exe_run_time(func):
    def wrapper(*args, **kw):
        local_time = time.time()
        func(*args, **kw)
        print(f'当前方法:{func.__name__}耗时：{time.time() - local_time}')

    return wrapper
