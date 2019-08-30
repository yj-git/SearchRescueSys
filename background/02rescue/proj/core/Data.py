from model import model
import os
import numpy as np
import netCDF4 as nc
import pandas as pd


class BaseData:
    '''
        所有data的父类，主要用来记录filename，dirpath等信息
    '''

    def __init__(self, dir, file):
        self.dir = dir
        self.file = file

    @property
    def fullpath(self):
        '''
            要读取的文件的全路径
        :return:
        '''
        return os.path.join(self.dir, self.fie)


class SearchRescueData(BaseData):
    '''
        本类直接操作nc文件，读取出搜救model需要的数据并写入mongo
    '''

    ds = None

    def __init__(self, dir: str, file: str):
        super(SearchRescueData, self).__init__(dir, file)

    # @staticmethod
    def init(self):
        '''
            根据fullpath，读取对应的文件
        :return:
        '''
        if (self.ds is not None):
            self.ds = nc.Dataset(self.fullpath)

    def checkNotMatchVariables(self, *args):
        '''
            获取不在ns的变量中的值
        :param args:
        :return:
        '''
        notMatchVariables = []
        notMatchVariables = [temp not in self.ds.variables.keys() for temp in args]
        return notMatchVariables

    def insert2DB(self):
        variables = ['lat', 'lon', 'time', 'x_wind', 'y_wind', 'y_sea_water_velocity', 'x_sea_water_velocity']
        notMatch = self.checkNotMatchVariables(variables)
        if (len(notMatch) == 0):
            # 没有不匹配的变量
            pass
