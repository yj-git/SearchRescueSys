#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/15 10:46
# @Author  : evaseemefly
# @Desc    :
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
        coverage_type_str: str = request.GET.get('type', None)
        coverage_area_str: str = request.GET.get('area', None)
        forecast_datetime_str: str = request.GET.get('current', None)
        coverage_type: int = int(coverage_type_str) if coverage_type_str is not None else DEFAULT_FK
        coverage_area: int = int(coverage_area_str) if coverage_area_str is not None else DEFAULT_FK
        forecast_datetime: datetime = arrow.get(
            forecast_datetime_str).datetime if forecast_datetime_str is not None else datetime.now()
        return coverage_type, coverage_area, forecast_datetime
