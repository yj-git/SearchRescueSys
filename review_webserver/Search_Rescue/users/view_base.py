from datetime import datetime
from typing import Tuple, List
from rest_framework.decorators import APIView, api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.models import User
from util.common import DEFAULT_FK
from util.enum import TaskStateEnum
from base.view_base import CoverageBaseView
from users.models import TaskUserModel


class CaseBaseView(APIView):
    def get_user(self, request):
        if hasattr(request, 'user'):
            user = getattr(request, 'user')
        return user


class TaskBaseView(CoverageBaseView):
    def get_task_coverage(self, request) -> List[TaskUserModel]:
        '''
            根据 request 中的 type+area -> user_taskinfo 中的记录并返回
        :param request:
        :return:
        '''
        # TODO:[*] 20-04-15 对于返回两个参数的方法如何加入类型约束？
        coverage_type, coverage_area = self.covert_request_typearea(request)
        return TaskUserModel.objects.filter(coverage_area=coverage_area, coverage_type=coverage_type,
                                            state=TaskStateEnum.COMPLETED.value).all()

        # if hasattr(request,'area') and hasattr(request,'type'):
