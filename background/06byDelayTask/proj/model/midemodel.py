#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/7 15:52
# @Author  : evaseemefly
# @Desc    :
# @Site    : 
# @File    : midemodel.py
# @Software: PyCharm
from typing import List
from common.enum import Area, ProductType


class AreaNameMidModel:
    '''
        区域与对应的名称re的 middle model
    '''

    def __init__(self, area: Area, re: str):
        self.area = area
        self.re = re


class ProductMidModel:
    '''
        产品与区域以及对应的名称re 的中间model
    '''

    def __init__(self, product_type: ProductType, area_names: List[AreaNameMidModel], root: str):
        self.product_type = product_type
        self.area_names = area_names
        self.root = root
