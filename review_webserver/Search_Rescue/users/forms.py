#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/24 5:46 下午
# @Author  : evaseemefly
# @Desc    :
# @Site    : 
# @File    : forms.py
# @Software: PyCharm
from django import forms


class CaseOilForm(forms.Form):
    wind_coefficient = forms.FloatField()
    wind_dir = forms.FloatField()
