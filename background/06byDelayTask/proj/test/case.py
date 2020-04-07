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


def main():
    current = datetime.now()
    init_product(current)
    coverage_current_job()
    pass


if __name__ == '__main__':
    main()
    pass
