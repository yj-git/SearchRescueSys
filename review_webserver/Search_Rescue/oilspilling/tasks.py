#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/23 7:07 下午
# @Author  : evaseemefly
# @Desc    : oil的延时任务
#            之前放在了 ./tasks_bakup/xx 中
# @Site    : 
# @File    : tasks_bakup.py
# @Software: PyCharm
from __future__ import absolute_import, unicode_literals
# 原生库
import os
from typing import List
# 第三方的库
from django.utils.timezone import now
from celery import shared_task

from tasks.tasks import Msg, JobState, NCJobBase, OilModelMsg, Event
# 本项目中
from oilspilling.middle_model import OilSpillingAvgMidModelbak
# 复用搜救中的models
from rescue.models import WindModel, CurrentModel
# apps -> user 中的models
from users.models import JobInfo, JobUserRate, AuthOilRela, CaseOilInfo
# 引入mongo model
from oilspilling.models import MassModel, OilModel, OilspillingAvgModel, OilSpillingModel
from util.common import get_path
from util.reader import OilFileReader, create_reader
from util.enum import JobTypeEnum, TaskStateEnum
# TODO:[*] 20-02-05 引发了一个错误，暂时去掉
from django.contrib.auth.models import User
from rela.views_base import RelaCaseOilView
# TODO:[-] 20-04-23 加入了celery的异步作业调度
from tasks.celery_con import app as celery_app
from base.tasks_base import TaskOpenDrift
from base.middle_model import TaskMsg
from util.customer_wrapt import provide_job_rate
from Search_Rescue.settings import _ROOT_DIR


def check_case_name(user_id: str, case_name: str) -> bool:
    '''
        根据指定user_id判断指定user_id是否已经创建了指定case_name
    :param user_id:
    :param case_name:
    :return:
    '''
    # TODO:[*] 20-02-05 引发了一个错误，暂时去掉
    users = User.objects.filter(id=user_id)
    if len(users) > 0:
        # 获取该用户的全部的case
        rela_user_case: List[AuthOilRela] = AuthOilRela.objects.filter(uid=users[0].id)
        case_names: List[str] = []
        if len(rela_user_case) > 0:
            # 获取所有的CaseInfo
            for temp in rela_user_case:
                if len(CaseOilInfo.objects.filter(id=temp.did_id))>0:
                    case_names.append(CaseOilInfo.objects.filter(id=temp.did.id)[0].case_code)
            # case_names = [CaseOilInfo().objects.filter(id=temp.did.id)[0].case_name for temp in rela_user_case]
        # 判断传入的case_name 是否存在在user的关系中
        if case_name in case_names:
            return True
        return False


class OilPyJob(NCJobBase):
    '''
        主要执行执行py作业脚本的操作
    '''

    @provide_job_rate(20, TaskStateEnum.RUNNING, JobTypeEnum.OIL)
    def handle_do_py(self, event: Event, **kwargs):
        print('模拟调用py文件，并传入相应参数')
        # TODO:[-] 20-04-30 获取传入的 attr￿s ，注意目前传入的 attrs 中缺少所需要的参数
        task_temp = TaskOpenDrift()
        task_msg: TaskMsg = kwargs.get('task_msg')
        # TODO:[-] 20-05-03 处理经纬度
        latlons = [float(temp) for temp in [task_msg.lat, task_msg.lon]]
        # TODO:[*] 20-04-30 此处有遗留
        task_temp.job(nc_files=task_msg.nc_files, latlon=latlons, start_time=task_msg.start_time,
                      end_time=task_msg.end_time, simluation_time_step=1800,
                      console_time_step=3600, out_file=task_msg.forecast_full_path,
                      export_variables=task_msg.export_variables)
        pass


class OilExistNcFile(NCJobBase):
    @provide_job_rate(50, TaskStateEnum.RUNNING, JobTypeEnum.OIL)
    def handle_check_file(self, event: Event, **kwargs):
        '''
            -1 根据msg获取指定的nc文件名称
            -2 读取指定的msg文件是否存在
            TODO:[-] 20-05-08 现已去掉，不再需要判断是否存在直接放在 中间model 中判断了
        :param msg:
        :return:
        '''
        # TODO:[*] 20-05-08 最新的修改，不再使用msg传递，使用attrs，其中包含了所需的全部数据
        task_msg: TaskMsg = kwargs.get('task_msg')
        # msg: Msg = kwargs.get('msg')
        finial_file = None
        # 文件名称为job_name+created
        # TODO:[*] 20-02-05 注意最后需要替换回去
        # merge_filename = f'{msg.job_name}{msg.created.strftime("%Y%m%d%H%M%S")}.nc'
        merge_filename = f'{msg.job_name}{msg.created.strftime("%Y%m%d")}.nc'
        # code=msg.job_name
        # 判断指定目录下的指定文件是否存在
        # 目录拼接规则: /root/user_id/yyyy/mm/
        merge_path = get_path(msg.user_id, msg.created)
        # 不存在指定路径则创建
        if not os.path.exists(merge_path):
            # D:\03data\oil
            # FileNotFoundError: [WinError 3]
            # 系统找不到指定的路径。: 'D:\\03data\\oil\\123\\2020\\02'
            # TODO:[*] 20-02-06 若不存在指定目录会报错？
            # 使用 os.makedirs 创建多层级目录，使用os.mkdir只能创建一层目录
            os.makedirs(merge_path)
            # os.mkdir(merge_path)
        if os.path.exists(os.path.join(merge_path, merge_filename)):
            # 将最终目录返回
            finial_file = os.path.join(merge_path, merge_filename)
            msg.dir_path = merge_path
        msg.file_name = merge_filename
        msg.msg.other['finial_file'] = finial_file

        pass


class OilReadNcJob(NCJobBase):
    @provide_job_rate(70, TaskStateEnum.RUNNING, JobTypeEnum.OIL)
    def handle_read_nc(self, event: Event, **kwargs):
        '''
            -3 存在读取获取每个时刻的均值
        :param msg:
        :return:
        '''
        # msg: Msg = kwargs.get('msg')
        #
        # finial_file = msg.msg.other['finial_file']
        task_temp = TaskOpenDrift()
        task_msg: TaskMsg = kwargs.get('task_msg')
        # 获取目标路径
        finial_file = task_msg.forecast_full_path
        # 使用xarray读取指定文件
        # 直接调用 util.reader直接读取并写入数据库
        reader_func = create_reader('file')
        reader = reader_func(task_msg.forecast_file_dir, task_msg.forecast_file_name)
        track_list = reader.read_avg_track(task_msg.case_code)
        # 存入msg中
        task_msg.track_list = track_list
        # 此处改为通过 task_msg传递
        # msg.msg.other['track_list'] = track_list


class OilDbJob(NCJobBase):
    '''
        -4 将每个时刻的均值写入数据
    '''

    @provide_job_rate(90, TaskStateEnum.RUNNING, JobTypeEnum.OIL)
    def handle_to_db(self, event: Event, **kwargs):
        '''

        :param msg:
        :return:
        '''
        # msg: Msg = kwargs.get('msg')
        task_temp = TaskOpenDrift()
        task_msg: TaskMsg = kwargs.get('task_msg')
        # 1- 判断指定case_name 是否存在于数据库中
        # 调用user app中的相应方法
        # TODO[*] 20-02-04 先给定一个写死的user_id
        user_id: str = task_msg.uid
        nc_file_name: str = None
        if task_msg is not None:
            is_match = check_case_name(user_id, task_msg.case_code)
            # TODO:[*] 20-05-11 由于逻辑修改此处注释掉
            # if is_match:
            #     # 若数据库中已经存在则直接从数据库中读取即可
            #     pass
            # else:
            #     # 若数据库中不存在则重新创建并写入数据
            #     # 调用父节点
            #     # 先把写入方法放在此处
            #     # 先将所有的平均轨迹点写入mongo，再在mysql中记录
            #     if task_msg.track_list:
            #         # if hasattr(msg.msg.other, 'track_list'):
            #         track_list: List[OilSpillingAvgMidModelbak] = task_msg.track_list
            #         # 取出track_list并写入mongoDb中
            #         for temp_track in track_list:
            #             self._create_model(temp_track)
            #             pass
            #     pass
            # TODO:[*] 20-05-11 此处逻辑重新修改，上面的判断全部去掉，因为case_code为加上时间戳的case所以不会有重复的问题，直接向mongo中写入即可
                # if hasattr(msg.msg.other, 'track_list'):
            track_list: List[OilSpillingAvgMidModelbak] = task_msg.track_list
            # 取出track_list并写入mongoDb中
            for temp_track in track_list:
                self._create_model(temp_track)
                pass
        pass

    def _create_model(self, oil_mid: OilSpillingAvgMidModelbak):

        current_temp = CurrentModel(x=getattr(oil_mid, 'x_sea_water_velocity'),
                                    y=getattr(oil_mid, 'y_sea_water_velocity'))
        wind_temp = WindModel(x=getattr(oil_mid, 'x_wind'),
                              y=getattr(oil_mid, 'y_wind'))
        point_temp = [round(getattr(oil_mid, 'point').get('lon'), 6),
                      round(getattr(oil_mid, 'point').get('lat'), 6)]
        time_temp = getattr(oil_mid, 'time')
        status_temp = getattr(oil_mid, 'status')
        code_temp = getattr(oil_mid, 'code')
        # 质量model
        mass_temp = MassModel(oil=getattr(oil_mid, 'mass_oil'),
                              evaporated=getattr(oil_mid, 'mass_evaporated'),
                              dispersed=getattr(oil_mid, 'mass_dispersed'))
        # 油的model
        # 有可能是masked的，所以需要判断
        oil_temp = OilModel(
            density=getattr(oil_mid, 'oil_film_thickness'),
            film_thickness=getattr(oil_mid, 'density'))

        wt_temp = getattr(oil_mid, 'sea_water_temperature')
        water_fraction = getattr(oil_mid, 'water_fraction')
        oil_avg_model = OilspillingAvgModel(time=time_temp, point=point_temp,
                                            code=code_temp, status=status_temp, current=current_temp,
                                            wind=wind_temp, wt=wt_temp, mass=mass_temp,
                                            water_fraction=water_fraction, oil=oil_temp
                                            )
        oil_avg_model.save()


class OilDoneJob(NCJobBase):
    @provide_job_rate(100, TaskStateEnum.COMPLETED, JobTypeEnum.OIL)
    def handle_to_done(self, event: Event, **kwargs):
        pass


# TODO:[-] 20-04-23 加入了 celery
# @celery_app.task(bind=True)
@shared_task
def do_job(attrs: {}):
    '''
        写入数据库只需要做如下工作：
                    -1 根据msg获取指定的nc文件名称
                    -2 读取指定的msg文件是否存在
                    -3 存在读取获取每个时刻的均值
                    -4 将每个时刻的均值写入数据
    '''
    job_oil = OilPyJob()
    # 不再需要check了，放在 middle_model 中了
    # job_check_nc_file = OilExistNcFile(job_oil)
    job_read_nc_file = OilReadNcJob(job_oil)
    job_db = OilDbJob(job_read_nc_file)
    job_done = OilDoneJob(job_db)
    # msg: Msg = Msg('code_test', 'test_case', '123', now(), JobState.RUNNING,
    #                r'D:\04git仓库\SearchRescueSys_new\SearchRescueSys\data\demo_data', OilModelMsg())
    task_msg = None
    if isinstance(attrs, TaskMsg):
        task_msg = attrs

    # TODO:[-] 20-02-04 注意此处只需要调用最终的那个job即可，不需要每个都调用
    # job_oil.handle(evt)
    # job_check_nc_file.handle(evt)
    # job_read_nc_file.handle(evt)
    for handle_name in ['do_py', 'read_nc', 'to_db', 'to_done']:
        evt = Event(handle_name)

        # TODO:[*] 20-05-08 以后不再操作msg，改为直接通过 task_msg 获取通信的message
        job_done.handle(evt, msg={}, task_msg=task_msg)
    pass
