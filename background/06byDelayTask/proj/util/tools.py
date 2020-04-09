#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/2 14:19
# @Author  : evaseemefly
# @Desc    : 所有的工具方法均放在此处
# @Site    : 
# @File    : tools.py
# @Software: PyCharm

import os
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
