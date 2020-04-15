#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/14 21:12
# @Author  : evaseemefly
# @Desc    :
# @Site    : 
# @File    : urls.py
# @Software: PyCharm

from django.conf.urls import url, include

from rest_framework import routers
from geo.views import CoverageInfoView

# from users import views

app_name = '[geo]'

urlpatterns = [
    url(r'^coverage/list/$', CoverageInfoView.as_view()),
]
