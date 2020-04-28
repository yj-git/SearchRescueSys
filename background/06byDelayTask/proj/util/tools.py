#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/2 14:19
# @Author  : evaseemefly
# @Desc    : 所有的工具方法均放在此处
# @Site    : 
# @File    : tools.py
# @Software: PyCharm

import os
import wrapt
import time
import datetime
from pathlib import Path


def check_path_exist(local_path: str):
    '''
        检查本地指定路径是否存在
    :param local_path:
    :return:
    '''
    if not os.path.exists(local_path):
        os.makedirs(local_path)


def check_file_exist(local_path: str, file_name: str):
    '''
        判断指定文件是否存在(上面方式也可以同时判断文件或文件夹，暂时保留)
    :param local_path:
    :param file_name:
    :return:
    '''
    file_temp = Path(os.path.join(local_path, file_name))
    return file_temp.is_file()

def exe_run_time():
    '''
        计算方法耗时的装饰器
    :return:
    '''
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        local_time = time.time()
        wrapped(*args, **kwargs)
        print(f'当前方法:{wrapped.__name__}耗时:{time.time() - local_time}')
    return wrapper

def utc_to_local(utc_st):
    '''
        UTC时间转本地时间（+8: 00）
    :param utc_st:
    :return:
    '''
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = utc_st + offset
    return local_st


def local_to_utc(local_st):
    '''
        本地时间转UTC时间（-8: 00）
    :param local_st:
    :return:
    '''
    time_struct = time.mktime(local_st.timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st