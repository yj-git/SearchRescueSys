#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/9 10:53
# @Author  : evaseemefly
# @Desc    : 操作netcdf等数据相关操作
# @Site    : 
# @File    : data.py
# @Software: PyCharm
# 系统库
import os
from abc import ABCMeta, abstractmethod
# numpy+netcdf4
import numpy as np
import netCDF4 as nc
from netCDF4 import Dataset
import pandas as pd
import numpy.ma as ma
import matplotlib as mpl
import matplotlib.pyplot as plt
import xarray as xar
# typing
from typing import List
# 本项目
from util.tools import check_file_exist, exe_run_time


class ICoverage4NC(metaclass=ABCMeta):
    '''
        所有 栅格数据的抽象父类
    '''

    def __init__(self, root_path: str, file_name: str, dimensions: List[str], variables: List[str]):
        self.root_path = root_path
        self.file_name = file_name
        self.dimensions = dimensions
        self.variables = variables
        self.ds_xr: Dataset = None

    @property
    def verification(self) -> bool:
        '''
            判断 nc 文件的合法性问题
        :return:
        '''
        return True

    # @exe_run_time()
    def load_data(self):
        '''
            大体流程:
                1- 判断指定文件是否存在
                2- 存在读取指定nc文件
                3- 合法性验证通过
                4- 为 -> self.ds_xr 赋值
        :return:
        '''
        # 1 TODO:[*] 20-04-09 此处需要写入日志
        if check_file_exist(self.root_path, self.file_name):
            # 2 读取
            # root_path:'D:\\01proj\\SearchRescueSys\\data\\download\\COMMON\\DAILY\\2020\\4\\9'
            # file_name:'bhs_cur_20200409.nc'
            ds_temp = xar.open_dataset(os.path.join(self.root_path, self.file_name))
            # 由于需要写入改为使用 netcdf4
            ds_temp = nc.Dataset(os.path.join(self.root_path, self.file_name), 'r+')
            if self.verification:
                # 验证通过为 -> self.ds_xr 赋值
                self.ds_xr = ds_temp
            pass

    @exe_run_time()
    @abstractmethod
    def modify_variable(self):
        '''
            需要由子类实现类实现的修订数据的方法
        :return:
        '''
        pass

    def init_modify(self):
        self.load_data()
        self.modify_variable()


class CurrentCoverage4NC(ICoverage4NC):
    def modify_variable(self):
        if self.ds_xr is not None:
            # 1- 修改 long_name
            self.ds_xr.variables['v'].long_name = 'Northward Water Velocity'
            self.ds_xr.variables['u'].long_name = 'Eastward Water Velocity'

            # 2- 修改 standard_name
            self.ds_xr.variables['v'].standard_name = 'y_sea_water_velocity'
            self.ds_xr.variables['u'].standard_name = 'x_sea_water_velocity'
        pass


class WindCoverage4NC(ICoverage4NC):
    '''
        TODO:[*] 20-04-09 暂缓实现 风场的数据
    '''

    def modify_variable(self):
        if self.ds_xr is not None:
            pass
