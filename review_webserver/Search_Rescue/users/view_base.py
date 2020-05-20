from datetime import datetime
from typing import Tuple, List, Dict
from rest_framework.decorators import APIView, api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from django.contrib.auth.models import User
import arrow
import pathlib

from util.common import DEFAULT_FK, DEFAULT_NULL_KEY
from util.enum import TaskStateEnum, JobTypeEnum
from util.customer_exception import LackCoverageError
from base.view_base import CoverageBaseView, get_val_from_request_data
from geo.views_base import CoverageBaseView as GeoCoverageView
from base.tasks_base import TaskOpenDrift
from base.middle_model import TaskMsg
from users.models import TaskUserModel, AuthOilRela, AuthRescueRela, CaseOilInfo, CaseRescueInfo, ICaseBaseModel, \
    JobInfo, JobUserRate, \
    ICaseBaseStore
from oilspilling.tasks import do_job
from rela.views_base import RelaCaseOilView
from .middle_model import JobMidModel
from Search_Rescue.settings import _ROOT_DIR


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

    def copy_request_2_attrs(self, request: Request, attrs: {}, **kwargs):
        '''
            将部分需要由 request.data 中获取的数据写入指定的字典 attrs 中
            注意: 需要传入 uid
        :param request:
        :param attrs:
        :return:
        '''
        uid = kwargs.get('uid')
        # 以后获取type_job 放在middle_model.py -> JobMidModel 中
        # type_job = int(type_job) if type_job is not None else JobTypeEnum.OIL.value
        # if type is not None:
        #     type = int(type)
        # TODO:[*] 20-02-25 以下部分建议改为通过model进行获取对应的参数，在model中添加验证方法，不用放在view
        # TODO:[*] 20-02-25 建议将root_path 与 case_path 通过工厂模式实现创建对应的 路径(路径不由前端传入，路径在后端根据传入的 user name 与当前的 yyyy/mm/dd 共同拼接而成。
        # eg: /user_name/yyyy/mm/dd/

        # TODO:[-] 20-05-12 注意修改此处的 case_path 是由传入的 start_time 决定的
        # TODO:[-] 20-05-19 此处的获取抽象至  base/view_base.py -> get_val_from_request_data 方法中
        # TODO:[-] 20-05-20 由于前后端存在字段名称不同的问题，需要加入前后端字段的映射,以下备注
        # ss = get_val_from_request_data(request, 'start_time')
        # attrs_names = ['create_date', 'forecast_date', 'case_name', 'case_desc', 'case_code', 'lat', 'lon', 'radius',
        #                'nums', 'simulation_duration', 'simulation_step', 'console_step', 'current_nondeterminacy',
        #                'equation', 'is_del', 'area', 'wind_coefficient', 'wind_dir', 'wind_coverage_id',
        #                'current_coverage_id', 'type']
        # for temp_name in attrs_names:
        #     attrs[temp_name] = get_val_from_request_data(request, temp_name)

        # TODO:[-] 20-05-20 由于前后端存在字段名称不同的问题，需要加入前后端字段的映射
        attrs_dicts: Dict[str, str] = {'simulation_step': 'simulationStep', 'console_step': 'consoleStep',
                                       'lat': 'lat', 'lon': 'lon',
                                       'forecast_date': 'forecastdate', 'nums': 'nums',
                                       'simulation_duration': 'duration', 'current_id': 'currentId',
                                       'wind_id': 'windId', 'type_job': 'goodType', 'radius': 'radius',
                                       'case_desc': 'caseDesc', 'case_code': 'caseName', 'case_name': 'caseName',
                                       'gmt_create': 'gmt_create', 'gmt_modified': 'gmt_modified', 'state': 'state'}
        for server, client in attrs_dicts.items():
            print(f'server:{server}|client:{client}')
            attrs[server] = get_val_from_request_data(request, client)

        # 获取起始时间
        start_time: datetime = arrow.get(get_val_from_request_data(request, 'forecastdate'))
        # 获取区域
        coverage_area = DEFAULT_NULL_KEY
        # TODO:[-] 20-05-20 只要传入了 wind_id 或 current 就查询该id对应的 geo_coverageinfo -> coverage_area
        for temp_coverage in [attrs.get('wind_id', None), attrs.get('current_id', None)]:
            if temp_coverage not in [None, DEFAULT_NULL_KEY]:
                coverage = GeoCoverageView()
                coverage_area = coverage.get_coverage(temp_coverage).coverage_area
        attrs['area'] = coverage_area
        users = User.objects.filter(id=uid)
        attrs['root_path'] = users[0].username
        attrs['user_name'] = users[0].username
        attrs['case_path'] = start_time.strftime('%Y/%m/%d')
        attrs['start_time'] = start_time
        # TODO:[-] 20-05-20 注意 end_time 是 start_time + 模拟时长
        attrs['end_time'] = arrow.get(start_time).shift(hours=attrs['duration'])
        pass

    def set_caseinfo(self, request, uid: str, attrs: {}):
        '''
            根据传入的 uid 与 request 添加或更新对应的case
        :param uid:
        :param request:
        :return:
        '''

        # 以下代码全部封装至 CaseBaseView -> copy_request_2_attrs 方法中

        # TODO:[*] 20-02-25此处验证操作放在 对应的 model中进行验证
        attrs = CaseOilInfo().validate(attrs)
        # 获取 oil or search
        type_job = attrs['type_job'] if attrs['type_job'] is not None else JobTypeEnum.OIL.value
        # 注意此处需要修改 request -> case_code ，修改为 attrs.get('case_code') 中的修改后的添加了时间戳的code
        # task_msg = self._copy_request_to_msg(attrs, uid=uid)
        try:
            if attrs is not None:
                # TODO:[-] 20-05-12 在此处生成 full_path (之前是写在 CaseOilInfo model 中的属性方法)
                def get_absolute_path(attrs) -> str:
                    # root_path 是第一级的目录 实际是 user_name
                    root_path = attrs.get('root_path', None)
                    case_path = attrs.get('case_path', None)
                    # file_name = attrs.get('file_name', None)
                    # root_path = getattr(attrs, 'root_path', None)
                    # case_path = getattr(attrs, 'case_path', None)
                    # file_name = getattr(attrs, 'file_name', None)
                    absolute_path = None
                    if any([root_path, case_path]) is None:
                        pass
                    else:
                        absolute_path = pathlib.Path(_ROOT_DIR) / root_path / 'FORECAST' / 'OIL' / case_path
                    return absolute_path

                absolute_path = get_absolute_path(attrs)
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
                                                         wind_dir=attrs['wind_dir'],
                                                         absolute_path=absolute_path,
                                                         ext='.nc'
                                                         )
                if case_result is not None:
                    # 建立User、Case关系
                    # 对于默认不传入type的应该设置为OilRela
                    if int(type_job) == JobTypeEnum.RESCUE.value:
                        model = AuthRescueRela
                    elif int(type_job) == JobTypeEnum.OIL.value:
                        model = AuthOilRela
                    else:
                        model = AuthOilRela
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

    def _create_job(self, attrs: {}):
        '''
            创建指定 jobinfo (对应表 user_jobinfo)
        :param job_mid:
        :type job_mid:
        :return:
        :rtype:
        '''
        jobinfo_result = JobInfo.objects.create(type=attrs['type_job'], job_celery_id='',
                                                case_code=attrs['case_code'],
                                                gmt_create=attrs['gmt_create'],
                                                gmt_modified=attrs['gmt_modified'], is_del=False,
                                                area=attrs['area'])
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

    def _copy_request_to_msg(self, request: {}, **kwargs) -> TaskMsg:
        '''
            将 request 传入的参数赋值给 TaskMsg 消息传递 中间model
        :param request:
        :type request:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        '''
        # 以下作为备份
        attrs = kwargs.get('attrs')

        uid = kwargs.get('uid')
        user_name = kwargs.get('user_name')
        # TODO:[*] 20-02-25 rate不由前端提交，首次创建完 user_jobinfo 后之后，在 user_jobuserrate 中添加对应的初始记录(此时rate应为0)，以后更新rate在后台中执行
        attrs['rate'] = 0
        attrs['uid'] = uid
        attrs['user_name'] = user_name

        # TODO:[-] 20-05-20 以下部分重构
        attrs['job_celery_id'] = request.GET.get('job_celery_id', None)
        # 以下为重复的变量
        # attrs['case_code'] = request.GET.get('case_code', None)
        # attrs['is_del'] = request.GET.get('is_del', None)
        # attrs['area'] = request.GET.get('area', None)
        # attrs['wind_id'] = request.GET.get('wind_id', None)
        # attrs['current_id'] = request.GET.get('current_id', None)
        # TODO:[-] 20-05-03 + 新加的 经纬度信息
        # attrs['lat'] = request.GET.get('lat', None)
        # attrs['lon'] = request.GET.get('lon', None)
        # attrs['type_job'] = request.GET.get('type', None)

        # TODO:[-] 20-05-20 已封装至 copy_request_2_attrs 方法中

        # TODO:[-] 20-05-20 由于之前在 set_caseinfo 中已经进行了读取，那么此处不需要再重复读取
        # attrs_dicts: Dict[str, str] = {'job_celery_id'}

        msg = TaskMsg()
        # 此处应改为直接拓展字典
        msg.attrs = attrs
        return msg

    def set_jobinfo(self, request, uid: str, **kwargs):
        '''
            根据传入的 uid 与 request 添加或更新对应的job
        :param uid:
        :param request:
        :return:
        '''
        case_id: int = kwargs.get('case_id')
        user_name: str = kwargs.get('user_name')
        # type_job = int(type_job) if type_job is not None else JobTypeEnum.OIL.value
        # TODO:[*] 20-02-25 此处需要对case_code进行加密(现在的case_code为 'xx')，需要在追加一个唯一的字符串 'xx'->'xx_afhjkashfjkas'，最好创建一个方法，根据时间戳或者其他方式生成唯一的字符串标识码
        # TODO:[*] 20-05-04 此种方式由于需要手动映射两次

        # 将 获取各类参数放在一个单独的方法中

        task_msg = self._copy_request_to_msg(request, uid=uid, user_name=user_name)

        # 不再使用 JobMidModel进行消息传递
        # job_mid: JobMidModel = JobMidModel(task_msg.case_code, task_msg.area, task_msg.type_job)
        try:
            attrs = JobInfo().validate(task_msg.attrs)
            if attrs is not None:
                # 创建JobInfo记录
                # TODO:[-] 20-02-25 添加JobInfo的同时还需要在 user_caseoilinfo 中添加相应记录——已在 set_caseinfo 方法中实现
                # TODO:[-] 20-05-07封装为 self._create_job
                jobinfo_result = self._create_job(attrs)
                task_msg.jid = jobinfo_result.id
                # attrs['jid'] = jobinfo_result.id
                # TODO:[*] 20-04-28 执行实际的 do job 操作，由于执行实际的 do_job 操作主要是在 oilspilling app -> tasks ，需要调用该延时task
                # TODO:[-] 20-04-30 注意前台传入时需要指定  风场 + 流场 的id!
                # TODO:[-] 20-05-07 此处封装在 self._insert_rela_case_oil 方法中
                temp_rela_ins = self._insert_rela_case_oil(case_id, task_msg.wind_id, task_msg.current_id)
                # 获取所有栅格数据( wind+current)的文件所在路径集合，并过滤掉所有None
                task_msg.nc_files = [temp_path for temp_path in [temp_rela_ins.get_coverage_path(temp_id) for temp_id in
                                                                 [task_msg.wind_id, task_msg.current_id]] if
                                     temp_path is not None]

                # 此处将之前传入的 attrs -> task_msg 实例对象
                self._do_job(attrs=task_msg)
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

    def _do_job(self, attrs: {}):
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
