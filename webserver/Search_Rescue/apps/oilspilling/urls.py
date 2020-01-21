from django.conf.urls import url, include
from django.urls import path
from .views import *

from rest_framework import routers

app_name = '[oilspilling]'
router = routers.DefaultRouter()
# router.register(r'test', TestViewset, base_name='test')
# 注意此处的base_name 改为了basename(可以看一下源码)
router.register(r'test', TestViewset, basename='test')

oils = TestViewset.as_view({
    'get': 'list'
})
urlpatterns = [
    # 获取指定日期的预报数据data/stationtide
    url(r'^track/$', OilSpillingTrackView.as_view()),
    url(r'^track/avg/$', OilSpillingTrackAvgView.as_view()),
    url(r'^realdata/avg/$', OilRealDataAvgView.as_view()),
    # 指定 date 与 code 的溢油 avg 的realdata
    url(r'^realdata/target/$', TargetDateRealDataView.as_view()),
    # 根据code获取指定的时间范围（date）
    url(r'^track/date/range/$', OilSpillingTrackAvgDateRangeView.as_view()),
    # url(r'^date/range/$',Rang)
    url(r'^create/model/$', CreateOilSpillingView.as_view()),
    # 商品列表页
    # re_path('^', include(router.urls)),
    # url(r'mytest/$',TestViewset.as_view(),name='oil')
    url(r'^api/', include(router.urls)),

    # 加入apiview的token验证
    url(r'testtoken/', TokenTestView.as_view())
]
urlpatterns += router.urls
