#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/7 15:53
# @Author  : evaseemefly
# @Desc    :
# @Site    : 
# @File    : enum.py
# @Software: PyCharm

from enum import Enum, unique


@unique
class ProductType(Enum):
    '''
        预报产品种类
    '''

    '''
        海面风
    '''
    WIND = 0
    '''
        海流
    '''
    CURRENT = 1


@unique
class Area(Enum):
    '''
        预报区域枚举
    '''

    '''
        西北太
    '''
    NORTHWEST = 0
    '''
        中国海
    '''
    CHINASEA = 1
    '''
        东中国海
    '''
    EASTCHINASEA = 2
    '''
        渤海
    '''
    BOHAISEA = 3
    '''
        印度洋
    '''
    INDIAN = 4
    '''
        南海
    '''
    SOUTHCHINASEA = 5

