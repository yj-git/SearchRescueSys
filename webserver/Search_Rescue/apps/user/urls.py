from django.conf.urls import url, include

from rest_framework import routers

from apps.user.views import UserListView, UserTestListView

app_name = '[user]'

urlpatterns = [
    url(r'^user/list/$', UserListView.as_view()),
    url(r'^user/test/$', UserTestListView.as_view()),
]
