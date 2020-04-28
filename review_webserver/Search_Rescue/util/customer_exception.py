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


class LackCoverageError(BaseSubmitDataError):
    pass
