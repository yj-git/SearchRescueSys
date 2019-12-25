import os

import numpy as np
import netCDF4 as nc
import pandas as pd
import numpy.ma as ma

import matplotlib as mpl
import matplotlib.pyplot as plt

import xarray as xar

from core.data import OilSpillingData
from common.common import exe_run_time

class BaseStep:
    '''
        step的父类
    '''

    def __init__(self, dir: str, file_name: str):
        self.dir = dir
        self.file_name = file_name

    @property
    def file_full_name(self):
        return os.path.join(self.dir, self.file_name)


class OilStep(BaseStep):
    #
    # def __init__(self,dir,filename):
    #     '''
    #
    #     :param dir:
    #     :param filename:
    #     '''
    #     self.dir=dir
    #     self.filename=filename
    '''
        用来保存读取的nc文件的 xaarray.Dataset
        TODO:[*] 19-12-25 此处需不需要使用with的方式打开？还是会自动释放？
    '''
    ds_xr = None

    @exe_run_time
    def do_job(self):
        # 1 读取文件并获取连续的时间
        if self._check_file_exist():
            self._read_nc()
            coords = self._get_coords(['lat', 'lon', 'time'])
            times = self._get_times()
            # 判断times是否为指定的长度
            if len(times) == 73:
                # 循环times
                for index, time in enumerate(times):
                    # 获取指定timestamp的所有factor的dataframe
                    xr_merage = self._creat_merage_targettime(index)
                    # 写入数据库
                    oil_temp = OilSpillingData(xr_merage, 'test1')
                    oil_temp.save_2_db()
                pass

    def _check_file_exist(self):
        '''
            1- 判断指定目录下是否存在指定文件,若不存在或出现权限及其他错误时也返回false
        :return:
        '''
        matched = False
        try:
            matched = os.path.isfile(self.file_full_name)
        except PermissionError:
            matched = False
        except:
            matched = False
        return matched

    def _read_nc(self):
        '''
            2- 读取文件
        :return:
        '''
        if self._check_file_exist():
            # ds = nc.Dataset(self.file_full_name)
            self.ds_xr = xar.open_dataset(self.file_full_name)

    def _get_coords(self, coords: []) -> []:
        '''
            3- 获取所有的维度信息（coords，不是dims）
            维度应该只保留 time|lon|lat 三部分
        :param coords: 关注的维度 str 数组
        :return:
        '''
        coords_str = []

        if self.ds_xr is not None:
            for temp in self.ds_xr.coords:
                if temp in coords:
                    coords_str.append(temp)
        return coords_str

    def _get_times(self) -> []:
        '''
            4- 获取时间维度的数组
                timestamp
        :return:
        '''
        times = self.ds_xr.coords.get('time')
        if times is not None:
            return times.values.tolist()
        return []

    def _creat_merage_targettime(self, index: int):
        # TODO:[*] 19-12-25 需要更改的要素
        factors = ['x_wind', 'y_wind', 'status', 'x_sea_water_velocity', 'y_sea_water_velocity', 'mass_oil',
                   'mass_evaporated', 'mass_dispersed', 'oil_film_thickness', 'density', 'sea_water_temperature',
                   'water_fraction']
        if len(factors) > 0:
            xr_first_temp = self.ds_xr.isel(time=index).get(factors[0])
        else:
            return None
        # 根据指定的特征合成对应的
        xr_merage = None
        for y, factor in enumerate(factors):
            if y == 0:
                xr_merage = xar.merge([xr_first_temp])
                continue
            xr_temp_now = self.ds_xr.isel(time=index).get(factor)
            xr_merage = xar.merge([xr_merage, xr_temp_now])
            # xr_temp_now = xr_merage
        return xr_merage.where(xr_merage < 2000).to_dataframe().dropna(how='any')
        # return xr_merage
