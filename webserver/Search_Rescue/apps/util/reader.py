from abc import ABCMeta, abstractmethod
import os

# numpy 相关
import numpy as np
import pandas as pd
import numpy.ma as ma
# 读取nc文件相关
import netCDF4 as nc
import xarray as xar


class IOilReader(metaclass=ABCMeta):
    @abstractmethod
    def init_dataset(self):
        pass

    @abstractmethod
    def check_vars_exist(self, var_temp):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def read_avg_track(self, code):
        pass


class OilDbReader(IOilReader):
    def __init__(self, root_path: str, file_name: str):
        self.root_path = root_path
        self.file_name = file_name
        self.xarr: xar = None

    @property
    def full_path(self):
        '''
             dir+filename
        :return:
        '''
        if None not in [self.root_path, self.file_name]:
            return os.path.join(self.root_path, self.file_name)
        return None

    def _init_dataset(self):
        if self.full_path is not None:
            # TODO:[*] 此处需要测试一下内存使用情况
            # 读取nc文件
            # self.ds = nc.Dataset(self.full_path)
            self.xarr = xar.open_dataset(self.full_path)

    @property
    def get_dims(self):
        '''
            获取nc 文件中的维度
        :return:
        '''
        if self.xarr is not None:
            return self.xarr.dims
        else:
            self._init_dataset()
            # TODO:[*] 此处这么写可能有问题，需要试一下
            return self.get_dims()

    def get_vars(self):
        '''
            获取nc文件中的 变量(Data variables)
        :return:
        '''
        if self.xarr is not None:
            return self.xarr.data_vars
        else:
            self._init_dataset()
            return self.get_vars()

    def read(self):
        pass

    def check_dims_exist(self, dims: []) -> bool:
        '''
            判断是否存在指定名称的维度
        :param dims:
        :return:
        '''
        pass

    def check_vars_exist(self, var_temp: str) -> bool:
        '''
            判断指定的 var (name)是否存在
        :param var_temp:
        :return:
        '''
        # 可以使用xarray.data_vars.keys()的方式获取 KeysView
        if var_temp in self.get_vars().keys():
            return True
        else:
            return False

    def read_avg_track(self, code):
        '''
            根据传入的code获取指定code的平均轨迹
        :param code:
        :return:
        '''
        # 判断status是否存在


class OilFileReader(IOilReader):
    def read(self):
        pass


def create_reader(type: str):
    if type == 'db':
        return OilDbReader
    elif type == 'file':
        return OilFileReader
