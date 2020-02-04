from django.shortcuts import render

from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.models import User

# 本项目的模块
from .serializers import UserSerializer
from .common import check_case_name

# 引入task中的任务
from apps.tasks.oil_task import do_job
# from apps.oilspilling.tasks.oil_task import do_job
# from apps.user.operate import check_case_name
# 尝试引入类型约束
from typing import List
# Create your views here.

# from .models import AuthUserDir,CaseInfo

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



class UserTestListView(APIView):
    def get(self, request):
        user_id = request.GET.get('userid',None)
        case_name = request.GET.get('casename',None)
        do_job()
        is_match = check_case_name(user_id, case_name)
        return Response(is_match)
