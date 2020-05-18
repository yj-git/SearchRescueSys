#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/15 10:46
# @Author  : evaseemefly
# @Desc    : TODO:[*] 20-04-19 抽象的父类，提供部分公共可用的方法
#            是否不用继承自APIView？一个是让继承的子类中，再继承APIView，以避免循环引用的问题，并加上I关键字
#            对于非继承APIView的父类需要约定一个命名规范
# @Site    : 
# @File    : view_base.py
# @Software: PyCharm
from typing import Tuple
from datetime import date, datetime

# 第三方库
import arrow

from rest_framework.decorators import APIView, api_view, authentication_classes, permission_classes
from rest_framework.response import Response

# 本项目
from util.common import DEFAULT_FK


class CoverageBaseView(APIView):
    def covert_request_typearea(self, request) -> Tuple[int, int, datetime]:
        '''
            根据 request -> type ,area 获取 type,area (int,int)
        Args:
            request ():

        Returns:

        '''
        coverage_type_str: str = request.GET.get('type', None)
        coverage_area_str: str = request.GET.get('area', None)
        forecast_datetime_str: str = request.GET.get('current', None)
        coverage_type: int = int(coverage_type_str) if coverage_type_str is not None else DEFAULT_FK
        coverage_area: int = int(coverage_area_str) if coverage_area_str is not None else DEFAULT_FK
        forecast_datetime: datetime = arrow.get(
            forecast_datetime_str).datetime if forecast_datetime_str is not None else datetime.now()
        return coverage_type, coverage_area, forecast_datetime


class NecessaryFactorsView:
    need_factors=['']
    def check_need_factors(self,request):
        '''
            根据request 判断是否在当前的必要的要素列表中
        :param request:
        :return:
        '''
        is_ok=False
        pass