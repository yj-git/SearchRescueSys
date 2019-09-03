from django.conf.urls import url, include
from django.urls import path
from .views import *

app_name = '[rescue]'
urlpatterns = [
    # 获取指定日期的预报数据data/stationtide
    url(r'^track/$', RescueTrackView.as_view()),
    url(r'^factorlist/$', FactorListView.as_view()),
]
