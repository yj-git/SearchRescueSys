from django.conf.urls import url, include
from rest_framework_jwt.views import verify_jwt_token, obtain_jwt_token

from rest_framework import routers

from .views import UserListView, UserDoJobListView, getCaseList

# from users import views

app_name = '[user]'

urlpatterns = [
    url(r'^user/list/$', UserListView.as_view()),
    url(r'^user/test/$', UserDoJobListView.as_view()),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^case/list/$', getCaseList),
    # 切换为 JWT 的验证token的方式
    url('api-token-auth/', obtain_jwt_token),
]
