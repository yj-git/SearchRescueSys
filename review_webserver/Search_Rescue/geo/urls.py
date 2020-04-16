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
from geo.views import CoverageListView, GeoInfoView, GeoServerView

# from users import views

app_name = '[geo]'

urlpatterns = [
    url(r'^coverage/list/$', CoverageListView.as_view()),
    url(r'^layer/info/$', GeoInfoView.as_view()),
    url(r'^server/list/$', GeoServerView.as_view()),
]
