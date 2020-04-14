#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/12 15:49
# @Author  : evaseemefly
# @Desc    :
# @Site    : 
# @File    : view_base.py
# @Software: PyCharm
from typing import Tuple
from abc import abstractmethod, ABCMeta


class IBaseSelectListView(metaclass=ABCMeta):
    def get_base_params(self, request):
        '''

        :param request:
        :return:
        '''
        type_str: str = request.GET.get('type', None)
        parent_str: int = request.GET.get('parent', None)
        parent: int = 0 if parent_str is None else int(parent_str)
        type_select: int = 0 if type_str is None else int(type_str)
        return parent, type_select
