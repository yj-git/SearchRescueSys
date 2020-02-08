from abc import ABCMeta, abstractmethod
import os
import sys
from datetime import datetime

from typing import List

# numpy 相关
import numpy as np
import pandas as pd
import numpy.ma as ma
# 读取nc文件相关
# import netCDF4 as nc
import xarray as xar
from oilspilling.middle_model import OilSpillingAvgMidModel, OilSpillingTrackMidModel, OilSpillingAvgMidModelbak
from util.tools import exe_run_time

from oilspilling.models import OilspillingAvgModel


class OilReaderBase:
    def __init__(self, root_path: str, file_name: str):
        self.root_path = root_path
        self.file_name = file_name

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def read_avg_track(self, code) -> List[OilSpillingAvgMidModelbak]:
        pass


class IOilReader(metaclass=ABCMeta):
    @abstractmethod
    def _init_dataset(self):
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


class IOilTrack(metaclass=ABCMeta):
    '''
        所有实现轨迹的子类需要手动实现的抽象方法
    '''

    @abstractmethod
    def read_avg_track(self, code) -> List[OilSpillingAvgMidModelbak]:
        pass


class IOilScatter(metaclass=ABCMeta):
    @abstractmethod
    def read_current_track(self, code: str, now: datetime):
        '''
            根据code与当前时间获取对应的散点
        :param code:
        :param now:
        :return:
        '''
        pass


class OilFileReader(OilReaderBase, IOilReader, IOilScatter):
    def __init__(self, root_path: str, file_name: str):
        # self.root_path = root_path
        # self.file_name = file_name
        super().__init__(root_path, file_name)
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
            # 加入判断文件是否存在的判断
            if os.path.isfile(self.full_path):
                self.xarr = xar.open_dataset(self.full_path).load()
            else:
                raise IOError

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
        return dims in self.xarr.coords.keys()

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

    # TODO:[*] 注意此处加入了统计时间的装饰器会影响返回的list(加入后返回list为空)
    @exe_run_time
    def read_avg_track_bak(self, code):
        '''
            根据传入的code获取指定code的平均轨迹
        :param code:
        :return:
        '''
        # list_date = [datetime.now()]
        list_avg_models = []
        factors = ['x_wind', 'y_wind', 'status', 'x_sea_water_velocity', 'y_sea_water_velocity', 'mass_oil',
                   'mass_evaporated', 'mass_dispersed', 'oil_film_thickness', 'density', 'sea_water_temperature',
                   'water_fraction']
        # 判断status是否存在
        if self.check_vars_exist('status'):
            # 若存在status，根据时间维度获取连续时间的有效散点的轨迹均值

            for index, temp_time in enumerate(self.get_coord('time')):
                xr_merge = None
                print(f'当前时间{temp_time}|{index}')

                # TODO:[-] 20-01-18 住一此处，按需加载对性能影响很重要，若全在全部的vals会导致读取速度变慢(只读取同一个factor也会变慢)
                xr_temp = self.xarr.isel(time=index)['status']
                # xr_temp = self.xarr.isel(time=index)
                # TODO:[*] 20-01-18 之前只读取的status，需要读取全部的factor
                # 方式1: dataarray->df->筛选
                # 当前方法: read_avg_track耗时：5.346711158752441
                # df_finial = xr_temp.where(xr_temp >= 0).to_dataframe().dropna(how='any')
                # df_finial = df_finial[df_finial.status <= 0]
                # TODO:[*] 20-01-18 使用多个where的方式，会不会影响效率？
                # 方式2: dataarray 多重条件搜索 -> dataframe ->dropna
                # 当前方法:read_avg_track耗时：5.772573709487915
                # 当前方法: read_avg_track耗时：5.840391635894775
                # 此耗时比较稳定了
                # df_finial = xr_temp.where(xr_temp >= 0).where(xr_temp < 1).to_dataframe().dropna(how='any')
                #
                # # 以上方式1+2均使用一下方式获取均值及status
                # lat_mean = df_finial['lat'].mean()
                # lon_mean = df_finial['lon'].mean()
                # status_mean = df_finial['status'].mean()

                # 方式3: DataArray 多重条件搜索-> dropna
                # 经测试，还是方式3的读取方式最快，大概耗时5.1s左右
                # 当前方法: read_avg_track耗时：5.108347415924072
                xr_filter = xr_temp.where(xr_temp >= 0).where(xr_temp < 1).dropna(dim='trajectory',
                                                                                  how='any')
                # xr_filter = xr_temp.where(xr_temp['status'] >= 0).where(xr_temp['status'] < 1).dropna(dim='trajectory',
                #                                                                                       how='any')
                # 当前方法: read_avg_track耗时：3.9484479427337646
                # 当前方法: read_avg_track耗时：3.828770637512207
                # xr_filter = xr_temp.where(xr_temp >= 0).dropna(dim='trajectory', how='any')
                lat_mean = xr_filter['lat'].mean().data.tolist()
                lon_mean = xr_filter['lon'].mean().data.tolist()
                # x_wind = xr_filter['x_wind'].mean().data.tolist()
                # y_wind = xr_filter['y_wind'].mean().data.tolist()
                # x_sea_water_velocity = xr_filter['x_sea_water_velocity'].mean().data.tolist()
                # y_sea_water_velocity = xr_filter['y_sea_water_velocity'].mean().data.tolist()
                # mass_oil = xr_filter['mass_oil'].mean().data.tolist()
                # mass_evaporated = xr_filter['mass_evaporated'].mean().data.tolist()
                # mass_dispersed = xr_filter['mass_dispersed'].mean().data.tolist()
                # oil_film_thickness = xr_filter['oil_film_thickness'].mean().data.tolist()
                # density = xr_filter['density'].mean().data.tolist()
                # sea_water_temperature = xr_filter['sea_water_temperature'].mean().data.tolist()
                # water_fraction = xr_filter['water_fraction'].mean().data.tolist()
                status_mean = xr_filter.mean().data.tolist()
                # TODO:[*] 20-01-17 注意此处的time_time.values为datetime64需要转换为datetime

                temp_ts = pd.Timestamp(temp_time.values)

                list_avg_models.append(
                    OilSpillingAvgMidModel(code, status_mean, {'lat': lat_mean, 'lon': lon_mean}, temp_ts))
                # list_avg_models.append(
                #     OilSpillingAvgMidModel(code, status_mean, {'lat': lat_mean, 'lon': lon_mean}, temp_ts, x_wind,
                #                            y_wind, x_sea_water_velocity, y_sea_water_velocity, mass_oil,
                #                            mass_evaporated, mass_dispersed, oil_film_thickness, density,
                #                            sea_water_temperature, water_fraction))

        return list_avg_models

    @exe_run_time
    def read_avg_track(self, code):
        # list_date = [datetime.now()]
        list_avg_models = []
        factors = ['x_wind', 'y_wind', 'status', 'x_sea_water_velocity', 'y_sea_water_velocity', 'mass_oil',
                   'mass_evaporated', 'mass_dispersed', 'oil_film_thickness', 'density', 'sea_water_temperature',
                   'water_fraction']
        # 判断status是否存在
        if self.check_vars_exist('status'):
            # 若存在status，根据时间维度获取连续时间的有效散点的轨迹均值

            for index, temp_time in enumerate(self.get_coord('time')):
                xr_merge = None
                print(f'当前时间{temp_time}|{index}')

                # TODO:[-] 20-01-18 住一此处，按需加载对性能影响很重要，若全在全部的vals会导致读取速度变慢(只读取同一个factor也会变慢)
                xr_temp = self.xarr.isel(time=index)
                # xr_temp = self.xarr.isel(time=index)
                # TODO:[*] 20-01-18 之前只读取的status，需要读取全部的factor
                # 方式1: dataarray->df->筛选
                # 当前方法: read_avg_track耗时：5.346711158752441
                # df_finial = xr_temp.where(xr_temp >= 0).to_dataframe().dropna(how='any')
                # df_finial = df_finial[df_finial.status <= 0]
                # TODO:[*] 20-01-18 使用多个where的方式，会不会影响效率？
                # 方式2: dataarray 多重条件搜索 -> dataframe ->dropna
                # 当前方法:read_avg_track耗时：5.772573709487915
                # 当前方法: read_avg_track耗时：5.840391635894775
                # 此耗时比较稳定了
                # df_finial = xr_temp.where(xr_temp >= 0).where(xr_temp < 1).to_dataframe().dropna(how='any')
                #
                # # 以上方式1+2均使用一下方式获取均值及status
                # lat_mean = df_finial['lat'].mean()
                # lon_mean = df_finial['lon'].mean()
                # status_mean = df_finial['status'].mean()

                # 方式3: DataArray 多重条件搜索-> dropna
                # 经测试，还是方式3的读取方式最快，大概耗时5.1s左右
                # 当前方法: read_avg_track耗时：5.108347415924072
                # 注意其中是包含全的特征的dataset
                xr_filter = xr_temp.where(xr_temp['status'] >= 0).where(xr_temp['status'] < 1).dropna(dim='trajectory',
                                                                                                      how='any')
                # xr_filter = xr_temp.where(xr_temp['status'] >= 0).where(xr_temp['status'] < 1).dropna(dim='trajectory',
                #                                                                                       how='any')
                # 当前方法: read_avg_track耗时：3.9484479427337646
                # 当前方法: read_avg_track耗时：3.828770637512207
                # xr_filter = xr_temp.where(xr_temp >= 0).dropna(dim='trajectory', how='any')
                lat_mean = xr_filter['lat'].mean().data.tolist()
                lon_mean = xr_filter['lon'].mean().data.tolist()
                x_wind = xr_filter['x_wind'].mean().data.tolist()
                y_wind = xr_filter['y_wind'].mean().data.tolist()
                x_sea_water_velocity = xr_filter['x_sea_water_velocity'].mean().data.tolist()
                y_sea_water_velocity = xr_filter['y_sea_water_velocity'].mean().data.tolist()
                mass_oil = xr_filter['mass_oil'].mean().data.tolist()
                mass_evaporated = xr_filter['mass_evaporated'].mean().data.tolist()
                mass_dispersed = xr_filter['mass_dispersed'].mean().data.tolist()
                oil_film_thickness = xr_filter['oil_film_thickness'].mean().data.tolist()
                density = xr_filter['density'].mean().data.tolist()
                sea_water_temperature = xr_filter['sea_water_temperature'].mean().data.tolist()
                water_fraction = xr_filter['water_fraction'].mean().data.tolist()
                status_mean = xr_filter['status'].mean().data.tolist()
                # TODO:[*] 20-01-17 注意此处的time_time.values为datetime64需要转换为datetime

                temp_ts = pd.Timestamp(temp_time.values)

                # list_avg_models.append(
                #     OilSpillingAvgMidModel(code, status_mean, {'lat': lat_mean, 'lon': lon_mean}, temp_ts))
                list_avg_models.append(
                    OilSpillingAvgMidModelbak(code, status_mean, {'lat': lat_mean, 'lon': lon_mean}, temp_ts, x_wind,
                                              y_wind, x_sea_water_velocity, y_sea_water_velocity, mass_oil,
                                              mass_evaporated, mass_dispersed, oil_film_thickness, density,
                                              sea_water_temperature, water_fraction))

        return list_avg_models

    def get_coord(self, dim: str):
        '''
            获取指定维度的全部值
        :param dim:
        :return:
        '''
        if self.xarr is not None:
            return self.xarr.coords[dim]
        else:
            self._init_dataset()
            return self.get_coord(dim)

    @property
    def times_count(self) -> int:
        '''
            获取time维度的长度
        :return:
        '''
        if self.xarr is None:
            self._init_dataset()
        if self.check_dims_exist('time'):
            # 若存在time的维度，则获取time的count
            return len(self.xarr.coords['time'])
        else:
            return 0

    @exe_run_time
    def read_current_track(self, code: str, now: datetime, **kwargs) -> []:
        list_track = []
        page_index = kwargs.get('page_index')
        page_count = kwargs.get('page_count')
        if self.xarr is None:
            self._init_dataset()
        # 根据datetime找到对应的time的index
        # 根据status获取散点
        # 获取对应时间的 DataArray
        # TODO:[*] 20-01-19 此处改为通过 时间维度直接获取对应的值，不再使用时间索引
        # xr_merge = xar.merge([self.xarr.isel(time=[60]).get('status')])
        try:
            xr_merge = xar.merge([self.xarr.sel(time=now).get('status')])
            # 将DataArray -> DataSet
            xr_merge = xr_merge.where(xr_merge >= 0).where(xr_merge < 1).to_dataframe().dropna(how='any')
            # TODO:[*] 20-01-21 此处加入了分页
            xr_merge = xr_merge[page_index * page_count:(page_index + 1) * page_count]
            for index in range(len(xr_merge)):
                # 将DataFrame -> Series
                row_data = xr_merge.iloc[index]
                # 将dataset 转成model

                # TODO:[-] 20-01-22 注意此处需要保持与之前的接口的兼容性，之前的接口返回的point是一个数组类型，point.coordinates
                # list_track.append(OilSpillingTrackMidModel(row_data['status'],
                #                                            {'lat': row_data['lat'], 'lon': row_data['lon']}))
                list_track.append(OilSpillingTrackMidModel(row_data['status'], {'coordinates': [row_data['lon'],
                                                                                                row_data['lat']]}))
                # print(str(row_data['status'])+":"+str(row_data['lon'])+":"+str(row_data['lat']))
                # print(index)
                # 使用列表推导
                # list_track = [OilSpillingTrackMidModel(xr_merge.iloc[index]['status'],
                #                                        {'lat': xr_merge.iloc[index]['lat'], 'lon': xr_merge.iloc[index]['lon']})
                #               for index in
                #               range(len(xr_merge))]

        except KeyError:
            print('不存在的key索引/时间超出范围')
            raise KeyError
        except:
            print(f'其他错误:{sys.exc_info()[0]}')
            raise

        return list_track

    def read_date_range(self, **kwargs) -> {}:
        '''
            获取当前的时间维度的范围
        :return:
        '''
        res = None
        if self.xarr is None:
            self._init_dataset()
        if self.check_dims_exist('time'):
            res = [pd.to_datetime(self.xarr.coords['time'].min().values), pd.to_datetime(
                self.xarr.coords['time'].max().values)]
        return res

    def read_track_count(self, dt: datetime) -> int:
        '''
            获取指定时间的散点
        :param dt:
        :return:
        '''
        count = 0
        if self.xarr is None:
            self._init_dataset()
        if self.check_dims_exist('time'):
            try:
                ds = self.xarr.sel(time=dt)['status']
                # TODO:[-] 20-01-22 注意此处一定需要对status的范围进行筛选
                count = len(ds.where(ds >= 0).where(ds < 1).to_dataframe().dropna(how='any'))
            except KeyError:
                print('时间超出索引范围')

        return count


class OilDbReader(OilReaderBase, IOilTrack):
    # def __init__(self,root_path:str,file_name:str):
    #     pass
    def read(self):
        pass

    def read_date_range(self, **kwargs):
        code = kwargs.get('code')
        # 根据time去重
        list_avg = OilspillingAvgModel.objects(
            code=code).distinct(field='time')
        if len(list_avg) > 0:
            list_avg = list(set(list_avg))
            # 排序
            list_avg.sort()
        return list_avg

    @exe_run_time
    def read_avg_track(self, code):
        # TODO:[*] 此处有一个问题，若queryset 没有查到值的话直接调用distinct会报错
        # TypeError distinct() got an unexpected keyword argument 'filed'
        list_avg = []
        try:
            # TODO:[*] 20-02-06 注意此处使用 .distinct获取的是该字段的所有不重复的集合！
            list_avg = OilspillingAvgModel.objects(code=code)
            # list_avg = OilspillingAvgModel.objects(code=code).distinct(field='time')
            # list_avg = list(set(list_avg))
            # list_avg = list(set(list_avg))
            #             # list_avg.sort()
        except Exception as e:
            print(e)
            pass
        return list_avg

        pass


def create_reader(type: str):
    if type == 'db':
        # OilDbReader()
        return OilDbReader
    elif type == 'file':
        # OilFileReader()
        # OilDbReader()
        return OilFileReader
