#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/7 16:24
# @Author  : evaseemefly
# @Desc    :
# @Site    : 
# @File    : case.py
# @Software: PyCharm
from datetime import datetime

from core.job import coverage_current_job, init_product

def case_test_coveragedownload():
    '''
        20-04-07 + 测试下载 current 栅格数据(date)
    :return:
    '''
    current = datetime.now()
    init_product(current)
    coverage_current_job()

def main():
    case_test_coveragedownload()
    pass


if __name__ == '__main__':
    main()
    pass
