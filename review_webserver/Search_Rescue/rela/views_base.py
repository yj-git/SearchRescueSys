#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/30 3:59 下午
# @Author  : evaseemefly
# @Desc    :
# @Site    : 
# @File    : views_base.py
# @Software: PyCharm
from util.common import DEFAULT_FK, DEFAULT_NULL_KEY
from .models import RelaCaseOilCoverageModel
from geo.views_base import CoverageBaseView


class RelaCaseOilView:
    def add_info(self, case_id: int, wind_id: int = DEFAULT_FK, current_id: int = DEFAULT_FK):
        '''
            -> rela_case_oil 写入记录 ，注意: wind 与 current 必须有一个是 非空(不需要再做判断了)
        :param case_id:
        :type case_id:
        :param wind_id:
        :type wind_id:
        :param current_id:
        :type current_id:
        :return:
        :rtype:
        '''
        RelaCaseOilCoverageModel.objects.create(case_id=case_id, wind_id=wind_id, current_id=current_id)

    def get_wind(self, wind_id: int):
        '''
            获取 对应 id 的 wind coverage info
        :param wind_id:
        :type wind_id:
        :return:
        :rtype:
        '''

        if wind_id != DEFAULT_NULL_KEY:
            return CoverageBaseView().get_coverage(wind_id)

    def get_coverage_path(self, id: int) -> str:
        '''
            根据 id 获取对应的 wind 栅格数据存储路径
        :param id:
        :type id:
        :return:
        :rtype:
        '''
        if self.get_wind(id):
            return CoverageBaseView().get_coverage_fullpath(id)
        return None
