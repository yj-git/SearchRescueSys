#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/1 16:15
# @Author  : evaseemefly
# @Desc    :
# @Site    : 
# @File    : main.py
# @Software: PyCharm
from common.exceptionLog import exception_containsparams, exception
from common.log import init_logger, logger


class CustomerExeCase:
    def __init__(self, name: str):
        self.name = name

    # @exception_containsparams(logger)
    @exception(logger)
    def zeroErr(self, index: int):
        print(index)
        # <__main__.CustomerExeCase object at 0x120c99290>
        print(self)
        print(self.name)
        10 / 0
        pass


@exception_containsparams(logger)
def case_customer_exception():
    index = 1 / 0
    pass


def main():
    case_customer_exception()
    errCls = CustomerExeCase('ceshi')
    errCls.zeroErr(5)
    pass


if __name__ == '__main__':
    main()
