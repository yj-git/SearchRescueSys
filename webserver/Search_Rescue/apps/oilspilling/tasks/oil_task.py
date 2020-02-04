# 原生库
import os
from typing import List
# 第三方的库
import numpy as np
import netCDF4 as nc
import pandas as pd
import numpy.ma as ma
import matplotlib as mpl
import matplotlib.pyplot as plt
import xarray as xr
from apps.oilspilling.tasks.tasks import Msg, JobState, NCJobBase, OilModelMsg, Event
# 本项目中
from apps.oilspilling.middle_model import OilSpillingAvgMidModelbak
# 复用搜救中的models
from apps.rescue.models import WindModel, CurrentModel
# 引入mongo model
from apps.oilspilling.models import MassModel, OilModel, OilspillingAvgModel, OilSpillingModel
from apps.util.common import get_path
from apps.util.reader import OilFileReader, create_reader

from Search_Rescue.settings import NC_OPTIONS
from apps.user.common import check_case_name


class OilPyJob(NCJobBase):
    '''
        主要执行执行py作业脚本的操作
    '''

    def handle_default(self, msg: Msg):
        print('模拟调用py文件，并传入相应参数')
        pass


class OilExistNcFile(NCJobBase):
    def handle_default(self, msg: Msg):
        '''
            -1 根据msg获取指定的nc文件名称
            -2 读取指定的msg文件是否存在
        :param msg:
        :return:
        '''
        finial_file = None
        # 文件名称为job_name+created
        merge_filename = f'{msg.job_name}{msg.created.strftime("%Y%m%d%H%M%S")}'
        # 判断指定目录下的指定文件是否存在
        # 目录拼接规则: /root/user_id/yyyy/mm/
        merge_path = get_path(msg.user_id, msg.created)
        # 不存在指定路径则创建
        if os.path.exists(merge_path):
            os.mkdir(merge_path)
        if os.path.exists(os.path.join(merge_path, merge_filename)):
            # 将最终目录返回
            finial_file = os.path.join(merge_path, merge_filename)
        msg.msg.other['finial_file'] = finial_file


class OilReadNcJob(NCJobBase):
    def handle_default(self, msg: Msg):
        '''
            -3 存在读取获取每个时刻的均值
        :param msg:
        :return:
        '''
        # 获取目标路径
        finial_file = msg.msg.other['finial_file']
        # 使用xarray读取指定文件
        # 直接调用 util.reader直接读取并写入数据库
        reader_func = create_reader('file')
        reader = reader_func(NC_OPTIONS['_ROOT_DIR'], NC_OPTIONS['_RESULT_FILE'])
        track_list = reader.read_avg_track('test')
        # 存入msg中
        msg.msg.other['track_list'] = track_list


class OilDbJob(NCJobBase):
    '''
        -4 将每个时刻的均值写入数据
    '''

    def handle_default(self, msg: Msg):
        '''

        :param msg:
        :return:
        '''
        # 1- 判断指定case_name 是否存在于数据库中
        # 调用user app中的相应方法
        # TODO[*] 20-02-04 先给定一个写死的user_id
        user_id: str = '1'
        nc_file_name: str = None
        if isinstance(msg.msg, OilModelMsg):
            is_match = check_case_name(user_id, msg.job_name)
            # if hasattr(msg.msg, 'other'):
            #     if hasattr(msg.msg.other, 'finial_file')
            #         nc_file_name = msg.msg.other.finial_file
            if is_match:
                # 若数据库中已经存在则直接从数据库中读取即可
                pass
            else:
                # 若数据库中不存在则重新创建并写入数据
                # 调用父节点
                # 先把写入方法放在此处
                if hasattr(msg.msg.other, 'track_list'):
                    track_list: List[OilSpillingAvgMidModelbak] = msg.msg.other['track_list']
                    # 取出track_list并写入mongoDb中
                    for temp_track in track_list:
                        self._create_model(temp_track)
                        pass
                pass
        pass

    def _create_model(self, df_mean: OilSpillingAvgMidModelbak):
        current_temp = CurrentModel(x=df_mean.get('x_sea_water_velocity'),
                                    y=df_mean.get('y_sea_water_velocity'))
        wind_temp = WindModel(x=df_mean.get('x_wind'),
                              y=df_mean.get('y_wind'))
        current_temp = CurrentModel(x=df_mean.get('x_sea_water_velocity'),
                                    y=df_mean.get('y_sea_water_velocity'))
        point_temp = [round(df_mean.get('lon').item(), 6),
                      round(df_mean.get('lat').item(), 6)]
        time_temp = df_mean.get('time')
        status_temp = df_mean.get('status')

        # 质量model
        mass_temp = MassModel(oil=df_mean.get('mass_oil'),
                              evaporated=df_mean.get('mass_evaporated'),
                              dispersed=df_mean.get('mass_dispersed'))
        # 油的model
        # 有可能是masked的，所以需要判断
        oil_temp = OilModel(
            density=df_mean.get('oil_film_thickness'),
            film_thickness=df_mean.get('density'))

        wt_temp = df_mean.get('sea_water_temperature')
        water_fraction = df_mean.get('water_fraction')
        oil_avg_model = OilspillingAvgModel(time=df_mean.time, point=[round(df_mean.get('lon').item(), 6),
                                                                      round(df_mean.get('lat').item(), 6)],
                                            code=self.code, status=df_mean.get('status'), current=current_temp,
                                            wind=wind_temp, wt=wt_temp, mass=mass_temp,
                                            water_fraction=water_fraction, oil=oil_temp
                                            )
        oil_avg_model.save()


def do_job():
    '''
        写入数据库只需要做如下工作：
                    -1 根据msg获取指定的nc文件名称
                    -2 读取指定的msg文件是否存在
                    -3 存在读取获取每个时刻的均值
                    -4 将每个时刻的均值写入数据
    '''
    # job_oil = OilPyJob()
    # job_check_nc_file = OilExistNcFile(job_oil)
    # job_read_nc_file = OilReadNcJob(job_check_nc_file)
    # job_db = OilDbJob(job_read_nc_file)
    # evt = Event('defalut')
    # job_oil.handle(evt)
    # job_check_nc_file.handle(evt)
    # job_read_nc_file.handle(evt)
    # job_db.handle(evt)
    pass
