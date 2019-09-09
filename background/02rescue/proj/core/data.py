from model import model
import os
import numpy as np
import netCDF4 as nc
import pandas as pd

# ----
# 导入项目中的包
from .operate import my_connet
from model import model


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
        return os.path.join(self.dir, self.file)


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
        if (self.ds is None):
            self.ds = nc.Dataset(self.fullpath)

    def checkNotMatchVariables(self, *args):
        '''
            获取不在ns的变量中的值
        :param args:
        :return:
        '''
        not_match_variables = []
        not_match_variables = [temp not in self.ds.variables.keys() for temp in list(args)[0]]
        return any(not_match_variables)

    def insert2DB(self):
        '''
            读取文件并写入mongo
        :return:
        '''
        variables = ['lat', 'lon', 'time', 'x_wind', 'y_wind', 'y_sea_water_velocity', 'x_sea_water_velocity']
        not_match = self.checkNotMatchVariables(variables)
        if (not_match is False):
            # 没有不匹配的变量
            # 获取需要的数据
            all_data = self.get_all_data('xwind')
            # 写入数据库
            # 1 先连接数据库
            my_connet()
            for i in range(len(all_data['lat'])):
                wind_temp = model.WindModel(x=all_data['xwind'][i], y=all_data['ywind'][i])
                current_temp = model.CurrentModel(x=all_data['xcurrent'][i], y=all_data['ycurrent'][i])
                # point = [all_data['lon'][i], all_data['lat'][i]]
                point = [round(all_data['lon'][i].item(), 2), round(all_data['lat'][i].item(), 2)]
                # point = [float(all_data['lon'][i]), float(all_data['lat'][i])]
                # 注意此处的是np.float32类型，需要转换为float使用 .item()即可
                # TODO:[-] 注意使用mongoengine中的预定义的point类型，只接受python原生的float类型，不支持float32类型
                search_model = model.SearchRescueModel(code=self.get_code,time=all_data['time'][i], point=point, current=current_temp,
                                                       wind=wind_temp, status=all_data['status'][i])
                # mongoengine.errors.ValidationError: ValidationError(SearchRescueModel:None) (Both
                #                                                                              values ([118.9177, 24.735289]) in point
                # must
                # be
                # float or int: ['point'])
                search_model.save()
            # pass

    def get_all_data(self, type):
        all_data_dict = {'lat': self.get_lat_data,
                         'lon': self.get_lon_data,
                         'time': self.get_time_data,
                         'xwind': self.get_xwind_data,
                         'ywind': self.get_ywind_data,
                         'status': self.get_status_data,
                         'xcurrent': self.get_xcurrent_data,
                         'ycurrent': self.get_ycurrent_data}
        return all_data_dict

    @property
    def get_lat_data(self):
        return self.ds['lat'][:][0].data

    # @property
    # def get_lat_data(self):
    #     return self.ds['lon'][:][0].data
    @property
    def get_code(self):
        return self.file.split('.')[0]

    @property
    def get_lon_data(self):
        return self.ds['lon'][:][0].data

    @property
    def get_time_data(self):
        # return self.ds['time'][:][0].data
        return nc.num2date(self.ds['time'][:], 'seconds since 1970-1-1 00:00:00')

    @property
    def get_xwind_data(self):
        return self.ds['x_wind'][:][0].data

    @property
    def get_ywind_data(self):
        return self.ds['y_wind'][:][0].data

    @property
    def get_status_data(self):
        return self.ds['status'][:][0].data

    @property
    def get_xcurrent_data(self):
        return self.ds['x_sea_water_velocity'][:][0].data

    @property
    def get_ycurrent_data(self):
        return self.ds['y_sea_water_velocity'][:][0].data
