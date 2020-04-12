from django.conf.urls import url, include
from common.views import SelectListView, SelectParentListView

app_name = '[common]'

urlpatterns = [
    url(r'^select/$', SelectListView.as_view()),
    url(r'^select/parent/$', SelectParentListView.as_view()),
]
