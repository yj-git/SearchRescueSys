#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/1 16:17
# @Author  : evaseemefly
# @Desc    :
# @Site    : 
# @File    : file.py
# @Software: PyCharm

import path
import os
from datetime import datetime
from abc import ABCMeta, abstractmethod
# 本项目的
from conf import settings


class IFileBase(metaclass=ABCMeta):
    # 参考 gsconfg 加入一个对于后缀(文件类型的约束)
    allowed_types = {
        'nc': 'NetCDF'
    }

    def __init__(self, url: str, path_dir: str, file_name: str):
        '''

        :param url:
        :param path_dir:
        :param file_name:
        '''
        self.url = url
        self.path_dir = path_dir
        self.file_name = file_name

    @property
    @abstractmethod
    def get_re(self) -> str:
        '''
            需要由子类实现的抽象方法——获取正则表达式
        :return:
        '''
        pass

    @property
    @abstractmethod
    def save_path(self) -> str:
        '''
            需要在每个具体实现类中实现 转存路径 的方法
        :return:
        '''
        pass

    @property
    def file_ext(self):
        '''
            将 file_name 截取获取后缀
        :return:
        '''
        splits = self.file_name.split('.')
        if len(splits) > 0:
            return splits[-1]
        else:
            raise IOError

    def match_files(self):
        pass

    def copy(self, target_path: str, target_file: str):
        '''
            复制
        :param target_path:
        :param target_file:
        :return:
        '''

        pass


class ICoverageFile(IFileBase):

    def __init__(self, url: str, path_dir: str, file_name: str):
        super().__init__(url, path_dir, file_name)

    @property
    def get_re(self) -> str:
        '''
            TODO:[*] 20-04-01 : 等待文件名称确定后再做具体修改
        :return:
        '''
        return ''

    @property
    @abstractmethod
    def save_path(self) -> str:
        pass


class WindCoverageFile(ICoverageFile):
    '''
        风场数据
    '''

    def __init__(self, url: str, path_dir: str, file_name: str, current: datetime):
        super().__init__(url, path_dir, file_name)
        self.current = current

    @property
    def save_path(self) -> str:
        '''
            大致思路放在一个公用的方法中，调用时根据参数返回最终的 path (相对路径)
            路径的命名规范如下：
                ROOT -> COMMON -> DAILY -> yyyy/mm/dd
        :return:
        '''
        save_dir = os.path.join(self.path_dir, 'COMMON', 'DAILY', self.current.date().year,
                                self.current.date().month, self.current.date().day)
        return save_dir


class CurrentCoverageFile(ICoverageFile):
    '''
        流场数据
    '''

    def __init__(self, url: str, path_dir: str, file_name: str, current: datetime, re_str: str = None):
        super().__init__(url, path_dir, file_name)
        self._re_str = re_str
        self.current = current

    @property
    def save_path(self) -> str:
        '''
            大致思路放在一个公用的方法中，调用时根据参数返回最终的 path (相对路径)
            路径的命名规范如下：
                ROOT -> COMMON -> DAILY -> yyyy/mm/dd
        :return:
        '''
        save_dir = os.path.join(self.path_dir, 'COMMON', 'DAILY', str(self.current.date().year),
                                str(self.current.date().month), str(self.current.date().day))
        return save_dir

    @property
    def get_re(self) -> str:
        if self._re_str is not None:
            return self._re_str
