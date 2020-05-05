#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/26 11:51 上午
# @Author  : evaseemefly
# @Desc    : 任务的父类任务(部分公共任务)
# @Site    : 
# @File    : tasks_base.py
# @Software: PyCharm
import sys
from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
import pathlib

from typing import List

# 引用的第三方库
from opendrift.readers import reader_netCDF_CF_generic
from opendrift.models.openoil import OpenOil


class ITaskBase:
    '''
        所有 task 的抽象父类
        所有的 task 都必须要实现 do_job 这个方法(主入口方法)
    '''

    def __init__(self):
        pass

    @abstractmethod
    def do_job(self, *args, **kwargs):
        pass


class TaskOpenDrift(ITaskBase):
    def __init__(self):
        pass

    def job(self, nc_files: List[str], latlon: List[float], start_time: datetime, end_time: datetime,
            simluation_time_step: int, console_time_step: int, out_file=None, export_variables: List[str] = [],
            radius=50,
            number=3000, wind_drfit_dactor=.2):
        '''
            执行 open_drift 作业
        :param nc_files: 风场+流场的nc文件所在路径(绝对路径集合)
        :type nc_files:
        :param latlon: 经纬度集合
        :type latlon:
        :param start_time: 起始时间
        :type start_time:
        :param end_time: 结束时间
        :type end_time:
        :param simluation_time_step: 模拟步长
        :type simluation_time_step:
        :param console_time_step: 输出步长
        :type console_time_step:
        :param out_file: 输出文件名(可选)
        :type out_file:
        :param export_variables: 输出的变量集合
        :type export_variables:
        :return:
        :rtype:
        '''
        drift_temp = OpenOil(loglevel=0)
        # wind + current 的场文件
        list_reader: List[reader_netCDF_CF_generic.Reader] = []
        for file_temp in nc_files:
            if pathlib.Path(file_temp).is_file():
                list_reader.append(reader_netCDF_CF_generic.Reader(file_temp))
        drift_temp.add_reader(list_reader)
        # TODO:[*] 20-04-26 起止时间还需要做一个判断
        # 可行办法1:
        # times: List[datetime, datetime] = [list_reader[0].start_time, list_reader[0].start_time + timedelta(hours=73)]
        # 可行办法2:
        # times: List[datetime, datetime] = [datetime(2020, 4, 10, 9, 0),
        #                                    datetime(2020, 4, 10, 9, 0) + timedelta(hours=73)]
        # 注意此处的 datetime 是包含时区的，需要去掉时区
        # 使用 .replace(tzinfo=None)
        times: List[datetime, datetime] = [start_time.replace(tzinfo=None), end_time.replace(tzinfo=None)]
        drift_temp.seed_elements(latlon[1], latlon[0], radius=radius, number=number, time=times,
                                 wind_drift_factor=wind_drfit_dactor)

        drift_temp.set_config('processes:dispersion', True)
        drift_temp.set_config('processes:evaporation', True)
        drift_temp.set_config('processes:emulsification', True)
        drift_temp.set_config('drift:current_uncertainty', .1)
        drift_temp.set_config('drift:wind_uncertainty', 1)

        drift_temp.run(end_time=list_reader[0].end_time, time_step=simluation_time_step,
                       time_step_output=console_time_step, outfile=out_file,
                       export_variables=export_variables)

        pass

    def do_job(self, *args, **kwargs):
        o = OpenOil(loglevel=0)  # Set loglevel to 0 for debug information

        # Arome atmospheric model
        reader_arome = reader_netCDF_CF_generic.Reader(
            o.test_data_folder() + '16Nov2015_NorKyst_z_surface/arome_subset_16Nov2015.nc')
        # Norkyst ocean model
        reader_norkyst = reader_netCDF_CF_generic.Reader(
            o.test_data_folder() + '16Nov2015_NorKyst_z_surface/norkyst800_subset_16Nov2015.nc')

        # Uncomment to use live data from thredds
        # reader_arome = reader_netCDF_CF_generic.Reader('http://thredds.met.no/thredds/dodsC/meps25files/meps_det_extracted_2_5km_latest.nc')
        # reader_norkyst = reader_netCDF_CF_generic.Reader('http://thredds.met.no/thredds/dodsC/sea/norkyst800m/1h/aggregate_be')

        # 传入一个风场+流场(两者非必须)数组
        o.add_reader([reader_norkyst, reader_arome])

        # Seeding some particles
        lon = 4.6;
        lat = 60.0;  # Outside Bergen

        # time = datetime(2015, 9, 22, 6, 0, 0)
        # 时间数组
        times: List[datetime, datetime] = [reader_arome.start_time,
                                           reader_arome.start_time + timedelta(hours=30)]
        # time = reader_arome.start_time

        # Seed oil elements at defined position and time
        o.seed_elements(lon, lat, radius=50, number=3000, time=times,
                        wind_drift_factor=.02)

        # Adjusting some configuration
        o.set_config('processes:dispersion', True)
        o.set_config('processes:evaporation', True)
        o.set_config('processes:emulsification', True)
        o.set_config('drift:current_uncertainty', .1)
        o.set_config('drift:wind_uncertainty', 1)

        # Running model
        # end_time 为结束时间
        # time_step 模拟步长
        # time_step_output 输出步长 单位均为s
        o.run(end_time=reader_norkyst.end_time, time_step=1800,
              time_step_output=3600, outfile='openoil.nc',
              export_variables=['mass_oil'])

        # Print and plot results
        print(o)
        # o.plot(background=['x_sea_water_velocity', 'y_sea_water_velocity'], buffer=.5)
        o.animation()
        o.animation(density=True, show_elements=False)
        # o.animation(filename='openoil_time_seed.gif')
        o.plot()
        # o.plot_property('mass_oil')
        # o.plot_property('x_sea_water_velocity')
