from django.conf.urls import url, include
from common.views import SelectListView
app_name='[common]'

urlpatterns = [
    url(r'^select/$', SelectListView.as_view()),
]