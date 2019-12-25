import time

def exe_run_time(func):
    def wrapper(*args, **kw):
        local_time = time.time()
        func(*args, **kw)
        print(f'当前方法:{func.__name__}耗时：{time.time() - local_time}')

    return wrapper