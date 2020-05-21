#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/28 3:05 下午
# @Author  : evaseemefly
# @Desc    : 自定义的异常
# @Site    : 
# @File    : customer_exception.py
# @Software: PyCharm

class BaseSubmitDataError(Exception):
    def __init__(self, message):
        self.message = message

    pass


class LackNecessaryFactorError(BaseSubmitDataError):
    '''
        缺少必要的要素异常
    '''
    pass

class LackNeedSubmitFactorsError(BaseSubmitDataError):
    '''
        缺少请求所需的必要要素
    '''
    pass

class LackCoverageError(BaseSubmitDataError):
    pass


class ConvertError(BaseSubmitDataError):
    '''
        转换异常
    '''
    pass
