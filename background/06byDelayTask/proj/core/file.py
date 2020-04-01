#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/1 16:17
# @Author  : evaseemefly
# @Desc    :
# @Site    : 
# @File    : file.py
# @Software: PyCharm

from abc import ABCMeta, abstractmethod


class IFileBase(metaclass=ABCMeta):
    # 参考 gsconfg 加入一个对于后缀(文件类型的约束)
    allowed_types = {
        'nc': 'NetCDF'
    }

    def __init__(self, url: str, path: str, file_name: str):
        '''

        :param url:
        :param path:
        :param file_name:
        '''
        self.url = url
        self.path = path
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


class CoverageFile(IFileBase):

    def __init__(self, url: str, path: str, file_name: str):
        super().__init__(url, path, file_name)

    @property
    def get_re(self) -> str:
        '''
            TODO:[*] 20-04-01 : 需要
        :return:
        '''
        return ''
