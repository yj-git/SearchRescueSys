from datetime import datetime

from rest_framework.decorators import APIView, api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.models import User
from util.jobs import ForecastJob
from util.customer_exception import LackCoverageError, ConvertError

# from typing import List

# 本项目的模块
from users.serializers import UserSerializer, CaseSerializer, CaseNumsMidSerializer
from users.models import AuthOilRela, AuthRescueRela, CaseOilInfo, CaseRescueInfo, ICaseBaseModel, JobInfo, JobUserRate, \
    ICaseBaseStore
from users.middle_model import JobInfoMidModel, CaseNumsMidModel
# from apps.user.common import check_case_name

# 引入task中的任务
# TODO:[*] 20-02-05 尝试将替换apps中的tasks为外置的tasks
# from apps.tasks_bakup.oil_task import do_job
# from tasks_bakup.oil_task import do_job
# from apps.oilspilling.tasks_bakup.oil_task import do_job
# from apps.user.operate import check_case_name
# from apps.user.common import check_case_name
# 尝试引入类型约束
from typing import List
# from apps.user.models import AuthUserDir, CaseInfo
from .models import AuthOilRela, CaseOilInfo
from .common import check_case_name
from users.serializers import JobMidSerializer
from users.view_base import CaseBaseView


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


# TODO:[*] 20-02-12 此处还是准备使用类视图的方式，有部分方法需要重用
class CaseListView(CaseBaseView):
    _status = 500

    def get(self, request):
        # uid = request.GET.get('uid', None)
        # 符合条件的 case_code 集合
        case_codes: List[str] = []
        cases: List[ICaseBaseModel] = []
        jobs_mid: List[JobInfoMidModel] = []
        if hasattr(request, 'user'):
            user = getattr(request, 'user')
            if user:
                uid = user.id
                type_case = request.GET.get('type', None)
                if type_case is not None:

                    try:
                        type = int(type_case)
                        if any([uid, type_case]) is not None:
                            # 不使用 直接获取对应的 case_code ，而是直接获取对应的 caseXXinfo
                            case_codes = self.get_casecodes(uid, type)
                            cases = self.get_caseinfo(uid, type)
                            if len(cases) > 0:
                                # 方式1：
                                # # 继续根据 code 从 user_jobinfo 中获取符合条件的jobinfo
                                # jobs: List[JobInfo] = JobInfo.objects.filter(case_code__in=case_codes)
                                # # 对于每个job查找其对应的rate，并倒叙找到rate最大的一个
                                # for job_temp in jobs:
                                #     rates = JobUserRate.objects.filter(jid__id=job_temp.id)
                                #     rate_temp: JobUserRate = rates.order('rate').desc()[0]
                                #     JobInfoMidModel(job_temp.gmt_create, )
                                # 方式2：
                                for case_temp in cases:
                                    jobs: List[JobInfo] = JobInfo.objects.filter(case_code=case_temp.case_code)
                                    # 对于每个job查找其对应的rate，并倒叙找到rate最大的一个
                                    for job_temp in jobs:
                                        rates = JobUserRate.objects.filter(jid__id=job_temp.id)
                                        rate_temp: JobUserRate = rates.order_by('rate').last()
                                        job_mid = JobInfoMidModel(job_temp.gmt_create, case_temp.case_name,
                                                                  rate_temp.state,
                                                                  job_temp.area, 'doing',
                                                                  rate_temp.rate, job_temp.case_code)
                                        jobs_mid.append(job_mid)

                    except:
                        pass

        json_data = JobMidSerializer(jobs_mid, many=True)
        return Response(json_data.data)

    def post(self, request):
        json_data = ''
        if hasattr(request, 'user'):
            user = getattr(request, 'user')
            if user:
                uid = user.id
                try:
                    case_result = self.set_caseinfo(request, uid)
                    job_result = self.set_jobinfo(request, uid, case_id=case_result.id)
                    if case_result is not None:
                        self._status = 200
                        json_data = case_result.case_code
                        # return Response(case_result.case_code)
                    if job_result is not None:
                        self._status = 200
                        json_data = job_result.case_code
                        # return Response(job_result.case_code)
                except LackCoverageError as e:
                    json_data = e.message
                except:
                    json_data = '发生异常错误'
                    # return Response(status=self._status)
                    pass

        return Response(json_data, status=self._status)


class CaseHistoryListView(CaseListView):

    def get_casehistory_distinct(self, uid: str, type: int) -> List[CaseNumsMidModel]:
        '''
            根据uid 与 type 获取对应的case的历史记录 每日的创建的case的次数
        :param uid:
        :param type:
        :return:
        '''
        list_case: List[ICaseBaseStore] = self.get_caseinfo(uid, int(type))
        list_res: List[CaseNumsMidModel] = []
        # 找到不同的时间
        list_date: List[datetime] = [case.create_date.date() for case in list_case]
        for temp in set(list_date):
            list_res.append(CaseNumsMidModel(temp, list_date.count(temp)))

        return list_res

    def get(self, request):
        type: str = request.GET.get('type', None)
        list_history: List[CaseNumsMidModel] = []
        if hasattr(request, 'user'):
            user = getattr(request, 'user')
            if user and type:
                # list = self.get_caseinfo(user.id, int(type))
                list_history = self.get_casehistory_distinct(user.id, int(type))
        json_data = CaseNumsMidSerializer(list_history, many=True)
        return Response(json_data.data)


# authentication_classes = (JSONWebTokenAuthentication,)
# permission_classes = (IsAuthenticated,)

class CaseModelView(CaseBaseView):
    # 状态码
    _status = 500

    def get(self, request):
        '''
            从 user_caseinfo表中找到对应的记录
            TODO:[*] 20-04-22 此处注意修改 不能写死CaseOilInfo ，因为还有搜救的表
        :param request:
        :type request:
        :return:
        :rtype:
        '''
        user = self.get_user(request)
        type = request.GET.get('type', None)
        code = request.GET.get('casecode', None)
        case_temp: CaseOilInfo = None
        if code:
            cases = CaseOilInfo.objects.filter(case_code=code)
            if len(cases) > 0:
                case_temp = cases[0]
        json_data = CaseSerializer(case_temp, many=False).data
        return Response(json_data)

    def post(self, request):
        '''
            将之前写在 CaseListView 中的 post 中的内容放在此 view->post 中
        :param request:
        :type request:
        :return:
        :rtype:
        '''
        json_data = ''
        if hasattr(request, 'user'):

            user = getattr(request, 'user')
            if user:
                uid = user.id
                try:
                    case_result = self.set_caseinfo(request, uid)
                    # TODO:[-] 20-04-30 注意需要手动修改 request.GET['case_code']
                    copy_request = request.GET.copy()
                    copy_request['case_code'] = case_result.case_code
                    request.GET = copy_request
                    # 若上面的 case_result 为Null 下面的语句就不用执行
                    job_result = self.set_jobinfo(request, uid,
                                                  case_result=case_result,
                                                  case_id=case_result.id) if case_result is not None else None
                    if case_result is not None:
                        self._status = 200
                        json_data = case_result.case_code
                        # return Response(case_result.case_code)
                    if job_result is not None:
                        self._status = 200
                        json_data = job_result.case_code
                    else:
                        json_data = f'创建指定case时出错'
                        # return Response(job_result.case_code)
                except LackCoverageError as e:
                    json_data = e.message
                except ConvertError as e:
                    json_data = e.message
                except:
                    json_data = '发生异常错误'
                    pass

        return Response(json_data, status=self._status)
