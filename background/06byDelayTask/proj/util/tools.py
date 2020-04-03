#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/2 14:19
# @Author  : evaseemefly
# @Desc    : 所有的工具方法均放在此处
# @Site    : 
# @File    : tools.py
# @Software: PyCharm

import os


def check_path_exist(local_path: str):
    '''
        检查本地指定路径是否存在
    :param local_path:
    :return:
    '''
    if not os.path.exists(local_path):
        os.makedirs(local_path)