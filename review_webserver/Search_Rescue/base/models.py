#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/16 10:04
# @Author  : evaseemefly
# @Desc    : 公共的 model，或存放公共的 choice
# @Site    : 
# @File    : models.py
# @Software: PyCharm
from django.db import models

# 参照 dict_base -> pid=300
CHOICE_GEO_TYPE = (
    (-1, 'DEFAULT'),
    (301, 'NetCDF')
)


# TODO:[-] 20-02-12 注意所有的抽象model命名时加上I(参考c#的接口命名规范)
class IIsDelModel(models.Model):
    is_del = models.BooleanField(default=False)

    class Meta:
        abstract = True
