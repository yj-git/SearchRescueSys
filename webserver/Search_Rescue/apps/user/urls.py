from django.conf.urls import url, include

from rest_framework import routers

from .views import UserListView

app_name = '[user]'

urlpatterns = [
    url(r'^user/list/$', UserListView.as_view()),
]
