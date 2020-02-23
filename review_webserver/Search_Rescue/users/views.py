from datetime import datetime

from rest_framework.decorators import APIView, api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.models import User
# from typing import List

# 本项目的模块
from users.serializers import UserSerializer, CaseSerializer, CaseNumsMidSerializer
from users.models import AuthOilRela, AuthRescueRela, CaseOilInfo, CaseRescueInfo, ICaseBaseModel, JobInfo, JobUserRate, \
    ICaseBaseStore
from users.middle_model import JobInfoMidModel, CaseNumsMidModel
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
from users.serializers import JobMidSerializer


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

    def get_casecode(self, uid: str, type: CHOICE_TYPE) -> List[str]:
        '''
            根据uid获取 case_oil_info表中的所有的case_code
        :param uid:
        :return:
        '''
        # by cwb 2020-02-20
        #if type == '0':
        if type == 0:
            model = AuthOilRela
        else:
            model = AuthRescueRela
        rela = model.objects.filter(uid_id=uid)
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
                if hasattr(rela_temp, 'did'):
                    case_temp: ICaseBaseModel = getattr(rela_temp, 'did')
                    cases.append(case_temp)
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
                            case_codes = self.get_casecode(uid, type)
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
                                                                  rate_temp.rate)
                                        jobs_mid.append(job_mid)

                    except:
                        pass

        json_data = JobMidSerializer(jobs_mid, many=True)
        return Response(json_data.data)

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
        root_path = request.GET.get('root_path', None)
        case_path = request.GET.get('case_path', None)
        temp_date = request.GET.get('create_date', None)
        if temp_date is not None:
            create_date = datetime.strptime(temp_date, '%Y-%m-%d %H:%M:%S')
        else:
            create_date = None
        temp_date = request.GET.get('forecast_date', None)
        if temp_date is not None:
            forecast_date = datetime.strptime(temp_date, '%Y-%m-%d %H:%M:%S')
        else:
            forecast_date = None
        case_name = request.GET.get('case_name', None)
        case_desc = request.GET.get('case_desc', None)
        case_code = request.GET.get('case_code', None)
        lat = request.GET.get('lat', None)
        if lat is not None:
            lat = float(lat)
        lon = request.GET.get('lon', None)
        if lon is not None:
            lon = float(lon)
        radius = request.GET.get('radius', None)
        if radius is not None:
            radius = float(radius)
        nums = request.GET.get('nums', None)
        if nums is not None:
            nums = int(nums)
        simulation_duration = request.GET.get('simulation_duration', None)
        if simulation_duration is not None:
            simulation_duration = float(simulation_duration)
        simulation_step = request.GET.get('simulation_step', None)
        if simulation_step is not None:
            simulation_step = float(simulation_step)
        console_step = request.GET.get('console_step', None)
        if console_step is not None:
            console_step = float(console_step)
        current_nondeterminacy = request.GET.get('current_nondeterminacy', None)
        if current_nondeterminacy is not None:
            current_nondeterminacy = float(current_nondeterminacy)
        equation = request.GET.get('equation', None)
        if equation is not None:
            equation = int(equation)
        is_del = request.GET.get('is_del', None)
        if is_del == '0':
            is_del = False
        elif is_del == '1':
            is_del = True
        else:
            is_del = None
        area = request.GET.get('area', None)
        wind_coefficient = request.GET.get('wind_coefficient', None)
        if wind_coefficient is not None:
            wind_coefficient = float(wind_coefficient)
        wind_dir = request.GET.get('wind_dir', None)
        if wind_dir is not None:
            wind_dir = float(wind_dir)
        try:
            if None not in [type, root_path, case_path, create_date, forecast_date, case_name, case_desc, case_code,
                    lat, lon, radius, nums, simulation_duration, simulation_step, console_step,
                    current_nondeterminacy, equation, is_del, area, wind_coefficient, wind_dir]:
                cases = self.get_caseinfo(uid, type)
                update_num = 0
                #如果存在相同的case_code的记录，则更新CaseOilInfo相关字段值
                if len(cases) > 0:
                    for case_temp in cases:
                        if case_temp.case_code == case_code:
                            update_num = CaseOilInfo.objects.filter(id=case_temp.id).update(root_path=root_path, case_path=case_path,
                                                                     create_date=create_date,
                                                                     forecast_date=forecast_date,
                                                                     case_name=case_name, case_desc=case_desc,
                                                                     case_code=case_code,
                                                                     lat=lat, lon=lon, radius=radius, nums=nums,
                                                                     simulation_duration=simulation_duration,
                                                                     simulation_step=simulation_step,
                                                                     console_step=console_step,
                                                                     current_nondeterminacy=current_nondeterminacy,
                                                                     equation=equation, is_del=is_del,
                                                                     area=area,
                                                                     wind_coefficient=wind_coefficient,
                                                                     wind_dir=wind_dir)

                            break
                # 如果不存在相同的case_code的记录，则创建CaseOilInfo记录
                if update_num == 0:
                    case_result = CaseOilInfo.objects.create(root_path=root_path, case_path=case_path,
                                                             create_date=create_date,
                                                             forecast_date=forecast_date,
                                                             case_name=case_name, case_desc=case_desc,
                                                             case_code=case_code,
                                                             lat=lat, lon=lon, radius=radius, nums=nums,
                                                             simulation_duration=simulation_duration,
                                                             simulation_step=simulation_step,
                                                             console_step=console_step,
                                                             current_nondeterminacy=current_nondeterminacy,
                                                             equation=equation, is_del=is_del,
                                                             area=area,
                                                             wind_coefficient=wind_coefficient,
                                                             wind_dir=wind_dir)

                    if type == 0:
                        model = AuthOilRela
                    else:
                        model = AuthRescueRela
                    rela = model.objects.filter(uid_id=uid, did_id=case_result.id)
                    if len(rela) == 0:
                        model.objects.create(uid_id=uid, did_id=case_result.id)
            if case_result is not None:
                return case_result
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
        job_celery_id = request.GET.get('job_celery_id', None)
        case_code = request.GET.get('case_code', None)
        temp_date = request.GET.get('gmt_create', None)
        if temp_date is not None:
            gmt_create = datetime.strptime(temp_date, '%Y-%m-%d %H:%M:%S')
        else:
            gmt_create = None
        temp_date = request.GET.get('gmt_modified', None)
        if temp_date is not None:
            gmt_modified = datetime.strptime(temp_date, '%Y-%m-%d %H:%M:%S')
        else:
            gmt_modified = None
        is_del = request.GET.get('is_del', None)
        if is_del is not None:
            if is_del == '0':
                is_del = False
            elif is_del == '1':
                is_del = True
            else:
                is_del = None
        area = request.GET.get('area', None)
        if area is not None:
            area = int(area)

        rate = request.GET.get('rate', None)
        if rate is not None:
            rate = int(rate)
        state = request.GET.get('state', None)
        if state is not None:
            state = int(state)
        try:
            if None not in [type, job_celery_id, case_code, gmt_create, gmt_modified, is_del, area]:
                # 如果存在相同的case_code的记录，则更新JobInfo相关字段值
                jobinfo_result = JobInfo.objects.filter(case_code=case_code)
                if len(jobinfo_result) > 0:
                    update_num = jobinfo_result.update(type=type, job_celery_id=job_celery_id, gmt_create=gmt_create,
                                                        gmt_modified=gmt_modified, is_del=is_del, area=area)
                    if update_num > 0:
                        return jobinfo_result
                else:
                    # 如果不存在相同的case_code的记录，则创建JobInfo记录
                    jobinfo_result = JobInfo.objects.create(type=type, job_celery_id=job_celery_id, case_code=case_code,
                                                        gmt_create=gmt_create, gmt_modified=gmt_modified, is_del=is_del, area=area)
                    if jobinfo_result is not None:
                        if None not in [state, rate]:
                            jobrate_result = JobUserRate.objects.create(uid_id=uid, jid_id=jobinfo_result.id, rate=rate, state=state,
                                                        gmt_create=gmt_create, gmt_modified=gmt_modified)
                            if jobrate_result is not None:
                                return jobinfo_result
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
