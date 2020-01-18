import time
import functools


def exe_run_time(func):
    '''
        计算方法时间的装饰器
    :param func:
    :return:
    '''

    @functools.wraps(func)
    def wrapper(*args, **kw):
        local_time = time.time()
        # 注意此处需要获取func的执行返回的方法并返回
        res = func(*args, **kw)
        print(f'当前方法:{func.__name__}耗时：{time.time() - local_time}')
        return res
    return wrapper
