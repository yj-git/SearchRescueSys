#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/8 11:07 上午
# @Author  : evaseemefly
# @Desc    :
# @Site    : 
# @File    : middle_model.py
# @Software: PyCharm
from typing import List
import types
from os import path
from pathlib import Path
from Search_Rescue.settings import _ROOT_DIR


class TaskMsg:
    def __init__(self, attrs: {} = {}):
        self._attrs: {} = attrs
        # TODO:[*] 20-05-11
        self._attrs['export_variables'] = ['x_wind', 'y_wind', 'status', 'x_sea_water_velocity', 'y_sea_water_velocity',
                                           'mass_oil',
                                           'mass_evaporated', 'mass_dispersed', 'oil_film_thickness', 'density',
                                           'sea_water_temperature',
                                           'water_fraction']

    @property
    def attrs(self):
        return self._attrs

    @attrs.setter
    def attrs(self, val):
        self._attrs.update(val)
        pass
        # self._attrs = val

    @property
    def celery_id(self):
        return self._attrs.get('job_celery_id', None)

    @celery_id.setter
    def celery_id(self, val):
        self._attrs['job_celery_id'] = val

    @property
    def case_code(self):
        return self._attrs.get('case_code', None)

    @case_code.setter
    def case_code(self, val):
        self._attrs['case_code'] = val

    @property
    def area(self):
        area_temp=self._attrs.get('area')
        if type(area_temp)==str:
            return int(area_temp)
        elif type(area_temp)==int:
            return area_temp


    @area.setter
    def area(self, val):
        self._attrs['area'] = val

    @property
    def rate(self):
        return self._attrs.get('rate', None)

    @rate.setter
    def rate(self, val):
        self._attrs['rate'] = val

    @property
    def state(self):
        return self._attrs.get('state', None)

    @state.setter
    def state(self, val):
        self._attrs['state'] = val

    @property
    def type_job(self):
        return self._attrs.get('type_job', None)

    @type_job.setter
    def type_job(self, val):
        self._attrs['type_job'] = val

    @property
    def uid(self):
        return self._attrs.get('uid', None)

    @uid.setter
    def uid(self, val):
        self._attrs['uid'] = val

    @property
    def start_time(self):
        return self._attrs.get('start_time', None)

    @start_time.setter
    def start_time(self, val):
        self._attrs['start_time'] = val

    @property
    def end_time(self):
        return self._attrs.get('end_time', None)

    @end_time.setter
    def end_time(self, val):
        self._attrs['end_time'] = val

    @property
    def lat(self):
        return self._attrs.get('lat', None)

    @lat.setter
    def lat(self, val):
        self._attrs['lat'] = val

    @property
    def lon(self):
        return self._attrs.get('lon', None)

    @lon.setter
    def lon(self, val):
        self._attrs['lon'] = val

    @property
    def jid(self):
        '''
            user_jobinfo 表中的 -> id
        :return:
        :rtype:
        '''
        return self._attrs.get('jid', None)

    @jid.setter
    def jid(self, val):
        self._attrs['jid'] = val

    @property
    def wind_id(self):
        '''
            对应的是 geo_coverageinfo 表
        :return:
        :rtype:
        '''
        return self._attrs.get('wind_id', None)

    @wind_id.setter
    def wind_id(self, val):
        self._attrs['wind_id'] = val

    @property
    def current_id(self):
        '''
            对应的是 geo_coverageinfo 表
        :return:
        :rtype:
        '''
        return self._attrs.get('current_id', None)

    @current_id.setter
    def current_id(self, val):
        self._attrs['current_id'] = val

    @property
    def nc_files(self) -> List[str]:
        '''
            对应的是 geo_coverageinfo 表
        :return:
        :rtype:
        '''
        return self._attrs.get('nc_files', [])

    @nc_files.setter
    def nc_files(self, val: List[str]):
        self._attrs['nc_files'] = val

    @property
    def forecast_file_dir(self) -> str:
        '''
            生成的预报产品的最终目录(不含名称)
        :return:
        :rtype:
        '''
        save_dir = path.join(_ROOT_DIR, str(self.uid), 'FORECAST', 'OIL', str(self.start_time.date().year),
                             str(self.start_time.date().month), str(self.start_time.date().day))
        # 需要判断是否存在指定路径，若不存在则创建
        nc_folder = Path(save_dir)
        if not nc_folder.exists():
            nc_folder.mkdir(parents=True, exist_ok=True)
        return save_dir

    # @forecast_file_dir.setter
    # def forecast_file_dir(self, val: str):
    #     '''
    #         生成的预报产品的最终目录(不含名称)
    #     :return:
    #     :rtype:
    #     '''
    #     self._attrs['forecast_file_dir'] = val

    @property
    def forecast_file_name(self):
        '''
            生成的预报产品的文件名称(含 ext)
        :return:
        :rtype:
        '''
        # 此处应根据 case_code 拼接 nc即可
        return '.'.join([self.case_code, 'nc'])
        # return self._attrs.get('forecast_file_name')

    # @forecast_file_name.setter
    # def forecast_file_name(self, val: str):
    #     self._attrs['forecast_file_name'] = val

    @property
    def forecast_full_path(self) -> str:
        '''
            生成的最终的预报文件路径(full path)
        :return:
        :rtype:
        '''
        return path.join(self.forecast_file_dir, self.forecast_file_name)

    @property
    def track_list(self):
        return self._attrs.get('track_list', None)

    @track_list.setter
    def track_list(self, val):
        self._attrs['track_list'] = val

    @property
    def export_variables(self) -> List[str]:
        '''
            调用 opendrift 的输入的参数,需要给个默认值
        :return:
        :rtype:
        '''
        return self._attrs.get('export_variables', None)

    @export_variables.setter
    def export_variables(self, val: List[str]):
        '''
            调用opendrift 时的输入参数(若不给定则是默认指定 status)
        :param val:
        :type val:
        :return:
        :rtype:
        '''
        self._attrs['export_variables'] = val
