from django.conf.urls import url, include
from django.urls import path
from .views import *

app_name = '[oilspilling]'
urlpatterns = [
    # 获取指定日期的预报数据data/stationtide
    url(r'^track/$', OilSpillingTrackView.as_view()),
    url(r'^track/avg/$', OilSpillingTrackAvgView.as_view()),
    url(r'^realdata/avg/$', OilRealDataAvgView.as_view()),
    # 指定 date 与 code 的溢油 avg 的realdata
    url(r'^realdata/target/$', TargetDateRealDataView.as_view()),
    # 根据code获取指定的时间范围（date）
    url(r'^track/date/range/$', OilSpillingTrackAvgDateRangeView.as_view())
]
