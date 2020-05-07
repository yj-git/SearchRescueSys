#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/30 4:15 下午
# @Author  : evaseemefly
# @Desc    :
# @Site    : 
# @File    : views_base.py
# @Software: PyCharm
from typing import List
from os import path
import pathlib
from .models import CoverageModel
from util.common import DEFAULT_FK, DEFAULT_NULL_KEY


class CoverageBaseView:
    def get_coverage(self, id: int) -> CoverageModel:
        '''
            根据id获取对应的 geo_coverageinfo 集合
        :param id:
        :type id:
        :return:
        :rtype:
        '''
        if id not in [DEFAULT_FK, DEFAULT_NULL_KEY]:
            return CoverageModel.objects.filter(id=id).first()
        return None

    def get_coverage_fullpath(self, id: int) -> str:
        '''
            根据传入的id 获取对应的 coverage 的存储路径(从 geo_coverageinfo表中读取)
        :param id:
        :type id:
        :return:
        :rtype:
        '''
        temp = self.get_coverage(id)
        if temp is not None:
            temp_path: str = path.join(temp.root_path, temp.relative_path, temp.file_name)
            if pathlib.Path(temp_path).is_file():
                return temp_path
