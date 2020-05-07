from datetime import datetime
from typing import Tuple, List
from rest_framework.decorators import APIView, api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from django.contrib.auth.models import User
from util.common import DEFAULT_FK, DEFAULT_NULL_KEY
from util.enum import TaskStateEnum, JobTypeEnum
from util.customer_exception import LackCoverageError
from base.view_base import CoverageBaseView
from base.tasks_base import TaskOpenDrift
from users.models import TaskUserModel, AuthOilRela, AuthRescueRela, CaseOilInfo, CaseRescueInfo, ICaseBaseModel, \
    JobInfo, JobUserRate, \
    ICaseBaseStore
from oilspilling.tasks import do_job
from rela.views_base import RelaCaseOilView
from .middle_model import JobMidModel


class CaseBaseView(APIView):
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

    def get_user(self, request):
        if hasattr(request, 'user'):
            user = getattr(request, 'user')
        return user

    def gen_casecode(self, code):
        '''
            根据传入的 code 参数，生成带时间戳的case_code编码
            TODO:[-] 放在model中
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
        type_job = request.GET.get('type', None)
        # 以后获取type_job 放在middle_model.py -> JobMidModel 中
        # type_job = int(type_job) if type_job is not None else JobTypeEnum.OIL.value
        # if type is not None:
        #     type = int(type)
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
        attrs['wind_coverage_id'] = request.GET.get('wind_coverage_id', None)
        attrs['current_coverage_id'] = request.GET.get('current_coverage_id', None)
        # TODO:[*] 20-02-25此处验证操作放在 对应的 model中进行验证
        attrs = CaseOilInfo.validate(self, attrs)
        # 注意此处需要修改 request -> case_code ，修改为 attrs.get('case_code') 中的修改后的添加了时间戳的code

        try:
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
                    if type_job == JobTypeEnum.OIL.value:
                        model = AuthOilRela
                    else:
                        model = AuthRescueRela
                    rela = model.objects.create(uid_id=uid, did_id=case_result.id)
                    if rela is not None:
                        return case_result
                    else:
                        return None
        except IntegrityError as e:
            print(e.args)
        except SQLAlchemyError as e:
            print(e.args)
        except Exception as e:
            print(e.args)
            pass
        return None
        # 注意此处不能使用finally 因为会在上面的 return 之后再返回 None
        # finally:
        #     return None

    def _create_job(self, job_mid: JobMidModel):
        '''
            创建指定 jobinfo (对应表 user_jobinfo)
        :param job_mid:
        :type job_mid:
        :return:
        :rtype:
        '''
        jobinfo_result = JobInfo.objects.create(type=job_mid.job_type_val, job_celery_id='',
                                                case_code=job_mid.case_code,
                                                gmt_create=datetime.utcnow(),
                                                gmt_modified=datetime.utcnow(), is_del=False,
                                                area=job_mid.area)
        return jobinfo_result

    def _insert_rate(self, job_mid: JobMidModel):
        pass

    def _insert_rela_case_oil(self, case_id: int, wind_id: int, current_id: int):
        '''
            向 rela_case_oil 表中插入关联
        :param case_id:
        :type case_id:
        :param wind_id:
        :type wind_id:
        :param current_id:
        :type current_id:
        :return:
        :rtype:
        '''
        temp_rela_ins = RelaCaseOilView()
        temp_rela_ins.add_info(case_id, wind_id=wind_id, current_id=current_id)
        return temp_rela_ins

    def set_jobinfo(self, request, uid: str, **kwargs):
        '''
            根据传入的 uid 与 request 添加或更新对应的job
        :param uid:
        :param request:
        :return:
        '''
        case_id: int = kwargs.get('case_id')
        type_job = request.GET.get('type', None)
        # type_job = int(type_job) if type_job is not None else JobTypeEnum.OIL.value
        # TODO:[*] 20-02-25 此处需要对case_code进行加密(现在的case_code为 'xx')，需要在追加一个唯一的字符串 'xx'->'xx_afhjkashfjkas'，最好创建一个方法，根据时间戳或者其他方式生成唯一的字符串标识码
        # TODO:[*] 20-05-04 此种方式由于需要手动映射两次
        attrs = {}
        attrs['job_celery_id'] = request.GET.get('job_celery_id', None)
        attrs['case_code'] = request.GET.get('case_code', None)
        attrs['gmt_create'] = request.GET.get('forecast_date', None)
        attrs['gmt_modified'] = request.GET.get('gmt_modified', None)
        attrs['is_del'] = request.GET.get('is_del', None)
        attrs['area'] = request.GET.get('area', None)
        # TODO:[*] 20-02-25 rate不由前端提交，首次创建完 user_jobinfo 后之后，在 user_jobuserrate 中添加对应的初始记录(此时rate应为0)，以后更新rate在后台中执行
        attrs['rate'] = 0
        attrs['state'] = request.GET.get('state', None)
        attrs['wind_id'] = request.GET.get('wind_id', None)
        attrs['current_id'] = request.GET.get('current_id', None)
        # TODO:[-] 20-05-03 + 新加的 经纬度信息
        attrs['lat'] = request.GET.get('lat', None)
        attrs['lon'] = request.GET.get('lon', None)
        # TODO:[*] 20-05-04 + 此处最好改为自动将 request.GET中的字典映射到attrs中
        attrs['start_time'] = request.GET.get('start_time', None)
        attrs['end_time'] = request.GET.get('end_time', None)
        attrs['uid'] = uid

        job_mid: JobMidModel = JobMidModel(attrs['case_code'], attrs['area'], type_job)
        try:
            attrs = JobInfo.validate(self, attrs)
            if attrs is not None:
                # 创建JobInfo记录
                # TODO:[-] 20-02-25 添加JobInfo的同时还需要在 user_caseoilinfo 中添加相应记录——已在 set_caseinfo 方法中实现
                # TODO:[-] 20-05-07封装为 self._create_job
                # jobinfo_result = JobInfo.objects.create(type=type_job, job_celery_id=attrs['job_celery_id'],
                #                                         case_code=attrs['case_code'],
                #                                         gmt_create=attrs['gmt_create'],
                #                                         gmt_modified=attrs['gmt_modified'], is_del=attrs['is_del'],
                #                                         area=attrs['area'])
                jobinfo_result = self._create_job(job_mid)
                attrs['jid'] = jobinfo_result.id
                # TODO:[*] 20-04-28 执行实际的 do job 操作，由于执行实际的 do_job 操作主要是在 oilspilling app -> tasks ，需要调用该延时task
                # TODO:[-] 20-04-30 注意前台传入时需要指定  风场 + 流场 的id!
                # TODO:[-] 20-05-07 此处封装在 self._insert_rela_case_oil 方法中
                # temp_rela_ins = RelaCaseOilView()
                # temp_rela_ins.add_info(case_id, wind_id=attrs['wind_id'], current_id=attrs['current_id'])
                temp_rela_ins = self._insert_rela_case_oil(case_id, attrs['wind_id'], attrs['current_id'])
                # 获取所有栅格数据( wind+current)的文件所在路径集合，并过滤掉所有None
                attrs['nc_files'] = [temp_path for temp_path in [temp_rela_ins.get_coverage_path(temp_id) for temp_id in
                                                                 [attrs['wind_id'], attrs['current_id']]] if
                                     temp_path is not None]

                self.__do_job(attrs=attrs)
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

        except IntegrityError as e:
            print(e.args)
        except SQLAlchemyError as e:
            print(e.args)
        except Exception as e:
            print(e.args)
            pass

    def __do_job(self, attrs: {}):

        # TODO:[*] 20-04-28,测试时先不使用延时调试
        # do_job.delay()
        do_job(attrs)


class TaskBaseView(CoverageBaseView):
    def get_task_coverage(self, request) -> List[TaskUserModel]:
        '''
            根据 request 中的 type+area -> user_taskinfo 中的记录并返回
        :param request:
        :type request:
        :return: user_taskinfo 表中的记录
        :rtype:
        '''
        # TODO:[*] 20-04-15 对于返回两个参数的方法如何加入类型约束？
        coverage_type, coverage_area, forecast_datetime = self.covert_request_typearea(request)
        # TODO:[*] 20-04-16 由于时间的问题，此处只能先暂时去掉
        return TaskUserModel.objects.filter(coverage_area=coverage_area, coverage_type=coverage_type,
                                            state=TaskStateEnum.COMPLETED.value).all()
        # return TaskUserModel.objects.filter(coverage_area=coverage_area, coverage_type=coverage_type,
        #                                     forecast_date=forecast_datetime,
        #                                     state=TaskStateEnum.COMPLETED.value).all()

        # if hasattr(request,'area') and hasattr(request,'type'):
