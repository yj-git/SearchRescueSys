# 包含部分通用的方法
from datetime import datetime
import os

ROOT_PATH = r''


def get_path(temp: str, dt: datetime):
    '''
        根据传入的时间与temp(一般为user_id）合成最终的路径 xx/temp/yyyy/mm
    :param dt:
    :return:
    '''
    return os.path.join(ROOT_PATH, temp, dt.strftime('%Y'), dt.strftime('%m'))
