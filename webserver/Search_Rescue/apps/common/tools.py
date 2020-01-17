import time

def exe_run_time(func):
    '''
        计算方法时间的装饰器
    :param func:
    :return:
    '''
    def wrapper(*args, **kw):
        local_time = time.time()
        func(*args, **kw)
        print(f'当前方法:{func.__name__}耗时：{time.time() - local_time}')

    return wrapper