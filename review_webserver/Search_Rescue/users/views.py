from rest_framework.decorators import APIView, api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.models import User
# from typing import List

# 本项目的模块
from users.serializers import UserSerializer, CaseSerializer
from users.models import AuthOilRela, AuthRescueRela, CaseOilInfo, CaseRescueInfo, ICaseBaseModel,JobInfo
from users.middle_model import JobInfoMidModel
# from apps.user.common import check_case_name

# 引入task中的任务
# TODO:[*] 20-02-05 尝试将替换apps中的tasks为外置的tasks
# from apps.tasks.oil_task import do_job
# from tasks.oil_task import do_job
# from apps.oilspilling.tasks.oil_task import do_job
# from apps.user.operate import check_case_name
# from apps.user.common import check_case_name
# 尝试引入类型约束
from typing import List
# from apps.user.models import AuthUserDir, CaseInfo
from .models import AuthOilRela, CaseOilInfo
from .common import check_case_name


# from apps.oilspilling.models import CurrentModel


# Create your views here.

# from .models import AuthUserDir,CaseInfo

# 本app用来处理 和用户操作相关的查询逻辑

class UserListView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        '''
            获取所有的User列表(actived的用户)
        :param request:
        :return:
        '''
        users_actived = User.objects.filter(is_active=True)
        json_data = UserSerializer(users_actived, many=True).data
        return Response(json_data)


class UserDoJobListView(APIView):
    def get(self, request):
        user_id = request.GET.get('userid', None)
        case_name = request.GET.get('casename', None)
        # do_job()
        is_match = check_case_name(user_id, case_name)
        # return Response(is_match)


@authentication_classes(['JSONWebTokenAuthentication'])
@permission_classes(['IsAuthenticated'])
@api_view(['GET'])
def getCaseList(request):
    '''
        获取指定用户的case list
    :param request:
    :return:
    '''
    # 此处暂时不需要加别的验证，已经加入了权限验证的功能，暂时不需要别的验证
    uid = request.user.id
    if uid is not None:
        pass
    rela_user_case: List[AuthOilRela] = AuthOilRela.objects.filter(uid_id=uid)
    case_list: List[CaseOilInfo] = []
    if len(rela_user_case) > 0:
        # 若存在关联的case
        case_list = [temp.did for temp in rela_user_case]
    json_data = CaseSerializer(case_list, many=True).data
    return Response(json_data)


CHOICE_TYPE = {
    0: 'CaseOilInfo',
    1: 'CaseRescueInfo'
}


# TODO:[*] 20-02-12 此处还是准备使用类视图的方式，有部分方法需要重用
class CaseListView(APIView):
    def get_casecode(self, uid: str, type: CHOICE_TYPE) -> List[str]:
        '''
            根据uid获取 case_oil_info表中的所有的case_code
        :param uid:
        :return:
        '''
        if type == '0':
            model = AuthOilRela
        else:
            model = AuthRescueRela
        rela = model.objects.filter(uid_id=uid)
        dids: List[ICaseBaseModel] = [temp_rela.did for temp_rela in rela]
        codes = [temp.case_code for temp in dids]
        return codes

    def get(self, request):
        uid = request.GET.get('uid', None)
        type_case = request.GET.get('type', None)
        # 符合条件的 case_code 集合
        case_codes: List[str] = []
        if any([uid, type_case]) is not None:
            case_codes = self.get_casecode(uid, type_case)
            if len(case_codes)>0:
                # 继续根据 code 从 user_jobinfo 中获取符合条件的jobinfo
                JobInfo.objects.filter()
        return Response(case_codes)

# authentication_classes = (JSONWebTokenAuthentication,)
# permission_classes = (IsAuthenticated,)
