from django.shortcuts import render

from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.models import User

# 本项目的模块
from .serializers import UserSerializer

# Create your views here.

# 本app用来处理 和用户操作相关的查询逻辑

class UserListView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        '''
            获取所有的User列表(actived的用户)
        :param request:
        :return:
        '''
        users_actived=User.objects.filter(is_active=True)
        json_data=UserSerializer(users_actived,many=True).data
        return Response(json_data)
