from datetime import datetime

from rest_framework.decorators import APIView, api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.models import User
from util.jobs import ForecastJob

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
class CaseListView(APIView):
    CHOICE_TYPE = {
        0: 'CaseOilInfo',
        1: 'CaseRescueInfo'
    }

    def get_casecodes(self, uid: str, type: CHOICE_TYPE) -> List[str]:
        '''
            根据uid获取 case_oil_info表中的所有的case_code
        :param uid:
        :return:
        '''
        # by cwb 2020-02-20
        # if type == '0':
        if type == 0:
            model = AuthOilRela
        else:
            model = AuthRescueRela
        rela = model.objects.filter(uid_id=uid)
        # 注意did 就是 user_authresuce_rela/ user_authoil_rela 关联表中对应的 user_caserescueinfo/user_caseoilinfo 中的 case_code
        dids: List[ICaseBaseModel] = [temp_rela.did for temp_rela in rela]
        codes = [temp.case_code for temp in dids]
        return codes

    def get_caseinfo(self, uid: str, type: CHOICE_TYPE) -> List[ICaseBaseModel]:
        '''
            根据传入的 uid 与 type 获取对应的case list
        :param uid:
        :param type:
        :return:
        '''
        cases: List[ICaseBaseModel] = []
        if type == 0:
            model = AuthOilRela
        else:
            model = AuthRescueRela
        relas = model.objects.filter(uid_id=uid)
        # 找到关联表->的case
        if len(relas) > 0:
            # 找到所有的有关的case info
            for rela_temp in relas:
                # TODO:[*] 20-03-06 此处我修改回来了，请注意！ caiwb 20-02-29
                if hasattr(rela_temp, 'did'):
                    case_temp: ICaseBaseModel = getattr(rela_temp, 'did')
                    cases.append(case_temp)
                # if hasattr(rela_temp, 'did_id'):
                #     case_temp: ICaseBaseModel = getattr(rela_temp, 'did_id')
                #     cases.append(case_temp)
        return cases

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

    def gen_casecode(self, code):
        '''
            根据传入的 code 参数，生成带时间戳的case_code编码
        :param code:
        :return:
        '''
        dt_ms = datetime.now().strftime('%Y%m%d%H%M%S%f')
        case_code = code + '_' + dt_ms
        return case_code

    def set_caseinfo(self, request, uid: str):
        '''
            根据传入的 uid 与 request 添加或更新对应的case
        :param uid:
        :param request:
        :return:
        '''
        type = request.GET.get('type', None)
        if type is not None:
            type = int(type)
        # TODO:[*] 20-02-25 以下部分建议改为通过model进行获取对应的参数，在model中添加验证方法，不用放在view
        # TODO:[*] 20-02-25 建议将root_path 与 case_path 通过工厂模式实现创建对应的 路径(路径不由前端传入，路径在后端根据传入的 user name 与当前的 yyyy/mm/dd 共同拼接而成。
        # eg: /user_name/yyyy/mm/dd/
        attrs = {}
        users = User.objects.filter(id=uid)
        attrs['root_path'] = users[0].username
        attrs['case_path'] = datetime.now().strftime('%Y/%m')
        attrs['create_date'] = request.GET.get('create_date', None)
        attrs['forecast_date'] = request.GET.get('forecast_date', None)
        attrs['case_name'] = request.GET.get('case_name', None)
        attrs['case_desc'] = request.GET.get('case_desc', None)
        attrs['case_code'] = request.GET.get('case_code', None)
        attrs['lat'] = request.GET.get('lat', None)
        attrs['lon'] = request.GET.get('lon', None)
        attrs['radius'] = request.GET.get('radius', None)
        attrs['nums'] = request.GET.get('nums', None)
        attrs['simulation_duration'] = request.GET.get('simulation_duration', None)
        attrs['simulation_step'] = request.GET.get('simulation_step', None)
        attrs['console_step'] = request.GET.get('console_step', None)
        attrs['current_nondeterminacy'] = request.GET.get('current_nondeterminacy', None)
        attrs['equation'] = request.GET.get('equation', None)
        attrs['is_del'] = request.GET.get('is_del', None)
        attrs['area'] = request.GET.get('area', None)
        attrs['wind_coefficient'] = request.GET.get('wind_coefficient', None)
        attrs['wind_dir'] = request.GET.get('wind_dir', None)
        try:
            # TODO:[*] 20-02-25此处验证操作放在 对应的 model中进行验证
            attrs = CaseOilInfo.validate(self, attrs)
            if attrs is not None:
                # 创建CaseOilInfo记录
                case_result = CaseOilInfo.objects.create(root_path=attrs['root_path'],
                                                         case_path=attrs['case_path'], create_date=attrs['create_date'],
                                                         forecast_date=attrs['forecast_date'],
                                                         case_name=attrs['case_name'], case_desc=attrs['case_desc'],
                                                         case_code=attrs['case_code'],
                                                         lat=attrs['lat'], lon=attrs['lon'], radius=attrs['radius'],
                                                         nums=attrs['nums'],
                                                         simulation_duration=attrs['simulation_duration'],
                                                         simulation_step=attrs['simulation_step'],
                                                         console_step=attrs['console_step'],
                                                         current_nondeterminacy=attrs['current_nondeterminacy'],
                                                         equation=attrs['equation'], is_del=attrs['is_del'],
                                                         area=attrs['area'], wind_coefficient=attrs['wind_coefficient'],
                                                         wind_dir=attrs['wind_dir'])
                if case_result is not None:
                    # 建立User、Case关系
                    if type == 0:
                        model = AuthOilRela
                    else:
                        model = AuthRescueRela
                    rela = model.objects.create(uid_id=uid, did_id=case_result.id)
                    if rela is not None:
                        return case_result
                    else:
                        return None
                else:
                    return None
        except:
            pass

    def set_jobinfo(self, request, uid: str):
        '''
            根据传入的 uid 与 request 添加或更新对应的job
        :param uid:
        :param request:
        :return:
        '''
        type = int(request.GET.get('type', None))

        # TODO:[*] 20-02-25 此处需要对case_code进行加密(现在的case_code为 'xx')，需要在追加一个唯一的字符串 'xx'->'xx_afhjkashfjkas'，最好创建一个方法，根据时间戳或者其他方式生成唯一的字符串标识码
        attrs = {}
        attrs['job_celery_id'] = request.GET.get('job_celery_id', None)
        attrs['case_code'] = request.GET.get('case_code', None)
        attrs['gmt_create'] = request.GET.get('gmt_create', None)
        attrs['gmt_modified'] = request.GET.get('gmt_modified', None)
        attrs['is_del'] = request.GET.get('is_del', None)
        attrs['area'] = request.GET.get('area', None)
        # TODO:[*] 20-02-25 rate不由前端提交，首次创建完 user_jobinfo 后之后，在 user_jobuserrate 中添加对应的初始记录(此时rate应为0)，以后更新rate在后台中执行
        attrs['rate'] = 0
        attrs['state'] = request.GET.get('state', None)
        try:
            attrs = JobInfo.validate(self, attrs)
            if attrs is not None:
                # 创建JobInfo记录
                # TODO:[-] 20-02-25 添加JobInfo的同时还需要在 user_caseoilinfo 中添加相应记录——已在 set_caseinfo 方法中实现
                jobinfo_result = JobInfo.objects.create(type=type, job_celery_id=attrs['job_celery_id'],
                                                        case_code=attrs['case_code'],
                                                        gmt_create=attrs['gmt_create'],
                                                        gmt_modified=attrs['gmt_modified'], is_del=attrs['is_del'],
                                                        area=attrs['area'])
                if jobinfo_result is not None:
                    jobrate_result = JobUserRate.objects.create(uid_id=uid, jid_id=jobinfo_result.id,
                                                                rate=attrs['rate'], state=attrs['state'],
                                                                gmt_create=attrs['gmt_create'],
                                                                gmt_modified=attrs['gmt_modified'])
                    if jobrate_result is not None:
                        return jobinfo_result
                    else:
                        return None
                else:
                    return None
        except:
            pass

    def post(self, request):
        if hasattr(request, 'user'):
            user = getattr(request, 'user')
            if user:
                uid = user.id
                try:
                    case_result = self.set_caseinfo(request, uid)
                    job_result = self.set_jobinfo(request, uid)
                    if case_result is not None:
                        return Response(case_result.case_code)
                    if job_result is not None:
                        return Response(job_result.case_code)
                except:
                    pass


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
