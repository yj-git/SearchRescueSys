from django.conf.urls import url, include
from django.urls import path
from .views import *

app_name = '[oilspilling]'
urlpatterns = [
    # 获取指定日期的预报数据data/stationtide
    url(r'^track/$', OilSpillingTrackView.as_view()),
    url(r'^track/avg/$', OilSpillingTrackAvgView.as_view()),
]
