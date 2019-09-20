from model import model
import os
import numpy as np
import netCDF4 as nc
import pandas as pd

# ----
# 导入项目中的包
from .operate import my_connet
from model import model
from conf import setting
import concurrent.futures

# 引入计时器
from .common import exe_run_time

class BaseData:
    '''
        所有data的父类，主要用来记录filename，dirpath等信息
    '''
    ds = None
    dict_dimension = {}

    def __init__(self, dir, file):
        self.dir = dir
        self.file = file

    @property
    def fullpath(self):
        '''
            要读取的文件的全路径
        :return:
        '''
        # TODO:[-] 注意python3之后，unicode改为decode了
        # unicode(self.dir, 'utf-8')
        # return os.path.join(self.dir.decode('utf-8'), self.file)
        return os.path.join(self.dir, self.file)

    def init(self):
        '''
            根据fullpath，读取对应的文件
        :return:
        '''
        # 初始化ds以及维度字典
        if (self.ds is None):
            self.ds = nc.Dataset(self.fullpath)
            print(self.ds)
            print('-----')
            print(self.ds.variables)
        if (self.dict_dimension == {}):
            self.init_dimensions_dict()

    def init_dimensions_dict(self):
        '''
            初始化维度字典
        :return:
        '''
        for index, temp in enumerate(self.ds.dimensions.values()):
            # print(temp)
            self.dict_dimension[temp.name] = temp

    def checkNotMatchVariables(self, *args):
        '''
            获取不在ns的变量中的值
        :param args:
        :return:
        '''
        not_match_variables = []
        not_match_variables = [temp not in self.ds.variables.keys() for temp in list(args)[0]]
        return any(not_match_variables)

    @property
    def get_code(self):
        return os.path.splitext(self.file)[0]

    @property
    def get_time_data(self):
        # return self.ds['time'][:][0].data
        return nc.num2date(self.ds['time'][:], 'seconds since 1970-1-1 00:00:00')


class BaseCorrdinateAxis:
    '''
        坐标轴父类，将溢油与搜救的获取坐标轴的方法抽象在此
        溢油的维度只有 trajectory 与 time 两个维度
    '''

    def __init__(self, dict_temp: {}):
        self.dict_dimension = dict_temp

    @property
    def get_x_time(self):
        '''
            获取 time 维度 的长度
        :return:
        '''
        # 正常有25个
        return self.dict_dimension['time'].size

    @property
    def get_y_trajectory(self):
        '''
            获取 轨迹 维度 的长度
        :return:
        '''
        # 正常有100组
        return self.dict_dimension['trajectory'].size


class SearchRescueData(BaseData, BaseCorrdinateAxis):
    '''
        本类直接操作nc文件，读取出搜救model需要的数据并写入mongo
    '''

    def __init__(self, dir: str, file: str):
        super(SearchRescueData, self).__init__(dir, file)
        super(SearchRescueData, self).__init__(self.dict_dimension)

    # @staticmethod
    # def init(self):
    #     '''
    #         根据fullpath，读取对应的文件
    #     :return:
    #     '''
    #     # 初始化ds以及维度字典
    #     if (self.ds is None):
    #         self.ds = nc.Dataset(self.fullpath)
    #         print(self.ds)
    #         print('-----')
    #         print(self.ds.variables)
    #     if (self.dict_dimension == {}):
    #         self.init_dimensions_dict()

    # def checkNotMatchVariables(self, *args):
    #     '''
    #         获取不在ns的变量中的值
    #     :param args:
    #     :return:
    #     '''
    #     not_match_variables = []
    #     not_match_variables = [temp not in self.ds.variables.keys() for temp in list(args)[0]]
    #     return any(not_match_variables)

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
            # all_data = self.get_all_data('xwind')
            # 写入数据库
            # 1 先连接数据库
            my_connet()
            # self.get_all_data()
            # for i in range(len(all_data['lat'])):
            #     wind_temp = model.WindModel(x=all_data['xwind'][i], y=all_data['ywind'][i])
            #     current_temp = model.CurrentModel(x=all_data['xcurrent'][i], y=all_data['ycurrent'][i])
            #     # point = [all_data['lon'][i], all_data['lat'][i]]
            #     point = [round(all_data['lon'][i].item(), 2), round(all_data['lat'][i].item(), 2)]
            #     # point = [float(all_data['lon'][i]), float(all_data['lat'][i])]
            #     # 注意此处的是np.float32类型，需要转换为float使用 .item()即可
            #     # TODO:[-] 注意使用mongoengine中的预定义的point类型，只接受python原生的float类型，不支持float32类型
            #     search_model = model.SearchRescueModel(time=all_data['time'][i], point=point, current=current_temp,
            #                                            wind=wind_temp, status=all_data['status'][i])
            #     # mongoengine.errors.ValidationError: ValidationError(SearchRescueModel:None) (Both
            #     #                                                                              values ([118.9177, 24.735289]) in point
            #     # must
            #     # be
            #     # float or int: ['point'])
            #     search_model.save()
            # TODO:[*] 19-09-06 此处重新修改了，因为要根据两维进行遍历所以上面的方式不再适用
            self.circulation(self.get_code)
            # pass

    def circulation_bak(self, code: str):
        '''
            循环写入
        :return:
        '''
        x_index = 0
        y_index = 0

        for y_trajectory_temp in range(self.get_y_trajectory - 1):
            # 0-99
            for x_time_temp in range(self.get_x_time - 1):
                # 0-24
                wind_temp = model.WindModel(x=self.ds['x_wind'][y_trajectory_temp, x_time_temp],
                                            y=self.ds['y_wind'][y_trajectory_temp, x_time_temp])
                current_temp = model.CurrentModel(x=self.ds['x_sea_water_velocity'][y_trajectory_temp, x_time_temp],
                                                  y=self.ds['x_sea_water_velocity'][y_trajectory_temp, x_time_temp])
                # point = [all_data['lon'][i], all_data['lat'][i]]
                point_temp = [round(self.ds['lon'][y_trajectory_temp, x_time_temp].item()),
                              round(self.ds['lat'][y_trajectory_temp, x_time_temp].item())]
                time_temp = self.get_time_data[x_time_temp]
                status_temp = self.ds['status'][y_trajectory_temp, x_time_temp]
                search_model = model.SearchRescueModel(time=time_temp, point=point_temp, current=current_temp,
                                                       wind=wind_temp, status=status_temp, code=code,
                                                       num=str(y_trajectory_temp))
                search_model.save()

                x_index = x_index + 1
            y_index = y_index + 1
            pass

    def circulation(self, code: str):
        '''
            循环写入
        :return:
        '''
        x_index = 0
        y_index = 0

        for x_time_temp in range(self.get_x_time - 1):
            # 0-99
            for y_trajectory_temp in range(self.get_y_trajectory - 1):
                # 0-24
                wind_temp = model.WindModel(x=self.ds['x_wind'][y_trajectory_temp, x_time_temp],
                                            y=self.ds['y_wind'][y_trajectory_temp, x_time_temp])
                current_temp = model.CurrentModel(x=self.ds['x_sea_water_velocity'][y_trajectory_temp, x_time_temp],
                                                  y=self.ds['x_sea_water_velocity'][y_trajectory_temp, x_time_temp])
                # point = [all_data['lon'][i], all_data['lat'][i]]
                point_temp = [round(self.ds['lon'][y_trajectory_temp, x_time_temp].item(), 6),
                              round(self.ds['lat'][y_trajectory_temp, x_time_temp].item(), 6)]
                time_temp = self.get_time_data[x_time_temp]
                status_temp = self.ds['status'][y_trajectory_temp, x_time_temp]
                search_model = model.SearchRescueModel(time=time_temp, point=point_temp, current=current_temp,
                                                       wind=wind_temp, status=status_temp, code=code,
                                                       num=str(y_trajectory_temp))
                search_model.save()
                y_index = y_index + 1
            # 对当前的时间对应的所有点进行平均
            # 0-24
            wind_temp = model.WindModel(x=self.ds['x_wind'][:].data[:].T[x_time_temp].mean(),
                                        y=self.ds['y_wind'][:].data[:].T[x_time_temp].mean())
            current_temp = model.CurrentModel(x=self.ds['x_sea_water_velocity'][:].data[:].T[x_time_temp].mean(),
                                              y=self.ds['x_sea_water_velocity'][:].data[:].T[x_time_temp].mean())
            point_temp = [round(self.ds['lon'][:].data[:].T[x_time_temp].mean().item(), 4),
                          round(self.ds['lat'][:].data[:].T[x_time_temp].mean().item(), 4)]
            time_temp = self.get_time_data[x_time_temp]
            status_temp = self.ds['status'][:].data[:].T[x_time_temp].mean()
            search_avg_model = model.SearchRescueAvgModel(time=time_temp, point=point_temp, current=current_temp,
                                                          wind=wind_temp, status=status_temp, code=code,
                                                          num=str(y_trajectory_temp))
            search_avg_model.save()
        x_index = x_index + 1
        pass

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
    def get_lon_data(self):
        return self.ds['lon'][:][0].data

    # @property
    # def get_time_data(self):
    #     # return self.ds['time'][:][0].data
    #     return nc.num2date(self.ds['time'][:], 'seconds since 1970-1-1 00:00:00')

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

    # TODO:[-] 19-09-18 此处已经封装至 BaseCorrdinateAxis 父类中
    # def init_dimensions_dict(self):
    #     '''
    #         初始化维度字典
    #     :return:
    #     '''
    #     for index, temp in enumerate(self.ds.dimensions.values()):
    #         # print(temp)
    #         self.dict_dimension[temp.name] = temp

    # @property
    # def get_y_trajectory(self):
    #     '''
    #         获取 轨迹 维度 的长度
    #     :return:
    #     '''
    #     # 正常有100组
    #     return self.dict_dimension['trajectory'].size

    # @property
    # def get_x_time(self):
    #     '''
    #         获取 time 维度 的长度
    #     :return:
    #     '''
    #     # 正常有25个
    #     return self.dict_dimension['time'].size
    #


class OilSpillingData(BaseData, BaseCorrdinateAxis):
    # 1 先连接数据库
    my_connet()
    _all_data_dict = {}

    def __init__(self, dir: str, file: str):
        BaseData.__init__(self, dir, file)
        BaseCorrdinateAxis.__init__(self, self.dict_dimension)
        # super(OilSpillingData, self).__init__(dir, file)
        # super(OilSpillingData, self).__init__(self.dict_dimension)

    def insert2DB(self):
        '''
            读取文件并写入mongo
        :return:
        '''
        variables = ['lat', 'lon', 'time', 'x_wind', 'y_wind', 'y_sea_water_velocity', 'x_sea_water_velocity',
                     'sea_water_temperature', 'mass_oil', 'mass_evaporated', 'mass_dispersed', 'water_fraction',
                     'density', 'oil_film_thickness']
        not_match = self.checkNotMatchVariables(variables)
        self.get_all_data()
        if (not_match is False):
            # 没有不匹配的变量
            # 写入数据库
            # 1 先连接数据库
            # my_connet()
            # self.get_all_data()
            #     # TODO:[-] 注意使用mongoengine中的预定义的point类型，只接受python原生的float类型，不支持float32类型
            # TODO:[*] 19-09-06 此处重新修改了，因为要根据两维进行遍历所以上面的方式不再适用
            self.circulation(self.get_code)

    def get_all_data(self):
        if self._all_data_dict == {}:
            self._all_data_dict = {'x_wind': self.ds['x_wind'],
                                   'y_wind': self.ds['y_wind'],
                                   'x_sea_water_velocity': self.ds['x_sea_water_velocity'],
                                   'y_sea_water_velocity': self.ds['y_sea_water_velocity'],
                                   'lon': self.ds['lon'],
                                   'lat': self.ds['lat'],
                                   'status': self.ds['status'],
                                   'mass_oil': self.ds['mass_oil'],
                                   'mass_evaporated': self.ds['mass_evaporated'],
                                   'mass_dispersed': self.ds['mass_dispersed'],
                                   'density': self.ds['density'],
                                   'oil_film_thickness': self.ds['oil_film_thickness'],
                                   'sea_water_temperature': self.ds['sea_water_temperature'],
                                   'water_fraction': self.ds['water_fraction']}
        # return self._all_data_dict

    @exe_run_time
    def circulation_trajectory(self, x_time_temp: int, code: str):
        for y_trajectory_temp in range(self.get_y_trajectory - 1):
            # 0-73
            wind_temp = model.WindModel(x=self._all_data_dict['x_wind'][y_trajectory_temp, x_time_temp],
                                        y=self._all_data_dict['y_wind'][y_trajectory_temp, x_time_temp])
            current_temp = model.CurrentModel(x=self._all_data_dict['x_sea_water_velocity'][y_trajectory_temp, x_time_temp],
                                              y=self._all_data_dict['y_sea_water_velocity'][y_trajectory_temp, x_time_temp])
            # point = [all_data['lon'][i], all_data['lat'][i]]
            point_temp = [round(self._all_data_dict['lon'][y_trajectory_temp, x_time_temp].item(), 6),
                          round(self._all_data_dict['lat'][y_trajectory_temp, x_time_temp].item(), 6)]
            time_temp = self.get_time_data[x_time_temp]
            status_temp = self._all_data_dict['status'][y_trajectory_temp, x_time_temp]
            # 质量model
            mass_temp = model.MassModel(oil=self._all_data_dict['mass_oil'][y_trajectory_temp, x_time_temp],
                                        evaporated=self._all_data_dict['mass_evaporated'][y_trajectory_temp, x_time_temp],
                                        dispersed=self._all_data_dict['mass_dispersed'][y_trajectory_temp, x_time_temp])
            # 油的model
            # TODO:[*] 19-09-19 注意self.ds['density']对数组进行索引是一个masked_array
            # 有可能是masked的，所以需要判断
            oil_temp = model.OilModel(
                density=self._all_data_dict['density'][y_trajectory_temp, x_time_temp] if self._all_data_dict['density'][
                                                                                  y_trajectory_temp, x_time_temp].mask == True else None,
                film_thickness=self._all_data_dict['oil_film_thickness'][y_trajectory_temp, x_time_temp] if
                self._all_data_dict['oil_film_thickness'][
                    y_trajectory_temp, x_time_temp].mask == True else None)

            wt_temp = self._all_data_dict['sea_water_temperature'][y_trajectory_temp, x_time_temp] if \
                self._all_data_dict['sea_water_temperature'][
                    y_trajectory_temp, x_time_temp].mask == True else None
            water_fraction = self._all_data_dict['water_fraction'][y_trajectory_temp, x_time_temp] if self._all_data_dict['water_fraction'][
                                                                                              y_trajectory_temp, x_time_temp].mask == True else None
            # TODO:[*] 19-09-19 此处的思路 若出现--的这种情况，直接跳过，不用save了
            # 若为np.nan 的话直接跳过，不处理
            if (wt_temp == np.nan) is False:
                oil_model = model.OilSpillingModel(time=time_temp, point=point_temp, current=current_temp,
                                                   wind=wind_temp, status=status_temp, code=code,
                                                   wt=wt_temp, mass=mass_temp, water_fraction=water_fraction,
                                                   oil=oil_temp)
                try:
                    oil_model.save()
                except Exception as err:
                    print(f'保存 oil_model 出现异常，出现异常位置[x:{x_time_temp},y:{y_trajectory_temp}]')

            # y_index = y_index + 1
        # 对当前的时间对应的所有点进行平均
        # 0-24
        wind_temp = model.WindModel(x=self._all_data_dict['x_wind'][:].T[x_time_temp].mean(),
                                    y=self._all_data_dict['y_wind'][:].T[x_time_temp].mean())
        current_temp = model.CurrentModel(x=self._all_data_dict['x_sea_water_velocity'][:].T[x_time_temp].mean(),
                                          y=self._all_data_dict['x_sea_water_velocity'][:].T[x_time_temp].mean())
        point_temp = [round(self._all_data_dict['lon'][:].T[x_time_temp].mean().item(), 4),
                      round(self._all_data_dict['lat'][:].T[x_time_temp].mean().item(), 4)]
        time_temp = self.get_time_data[x_time_temp]
        status_temp = self._all_data_dict['status'][:].T[x_time_temp].mean()
        # 质量model
        mass_temp = model.MassModel(oil=self._all_data_dict['mass_oil'][:].T[x_time_temp].mean(),
                                    evaporated=self._all_data_dict['mass_evaporated'][:].T[x_time_temp].mean(),
                                    dispersed=self._all_data_dict['mass_dispersed'][:].T[x_time_temp].mean())
        # 油的model
        oil_temp = model.OilModel(density=self._all_data_dict['density'][:].T[x_time_temp].mean(),
                                  film_thickness=self._all_data_dict['oil_film_thickness'][:].T[x_time_temp].mean())

        wt_temp = self._all_data_dict['sea_water_temperature'][:].T[x_time_temp].mean()
        water_fraction = self._all_data_dict['water_fraction'][:].T[x_time_temp].mean()
        oil_avg_model = model.OilspillingAvgModel(time=time_temp, point=point_temp, current=current_temp,
                                                  wind=wind_temp, status=status_temp, code=code,
                                                  wt=wt_temp, mass=mass_temp, water_fraction=water_fraction,
                                                  oil=oil_temp)
        try:
            oil_avg_model.save()
        except Exception as err:
            print(f'保存avg出现异常，出现异常位置[x:{x_time_temp},y:{y_trajectory_temp}]')

        print(f'[-] 当前处理第:{x_time_temp},共:{self.get_x_time - 1}')

    def circulation_trajectory_bak(self, x_time_temp: int, code: str):
        for y_trajectory_temp in range(self.get_y_trajectory - 1):
            # 0-73
            wind_temp = model.WindModel(x=self.ds['x_wind'][y_trajectory_temp, x_time_temp],
                                        y=self.ds['y_wind'][y_trajectory_temp, x_time_temp])
            current_temp = model.CurrentModel(x=self.ds['x_sea_water_velocity'][y_trajectory_temp, x_time_temp],
                                              y=self.ds['y_sea_water_velocity'][y_trajectory_temp, x_time_temp])
            # point = [all_data['lon'][i], all_data['lat'][i]]
            point_temp = [round(self.ds['lon'][y_trajectory_temp, x_time_temp].item(), 6),
                          round(self.ds['lat'][y_trajectory_temp, x_time_temp].item(), 6)]
            time_temp = self.get_time_data[x_time_temp]
            status_temp = self.ds['status'][y_trajectory_temp, x_time_temp]
            # 质量model
            mass_temp = model.MassModel(oil=self.ds['mass_oil'][y_trajectory_temp, x_time_temp],
                                        evaporated=self.ds['mass_evaporated'][y_trajectory_temp, x_time_temp],
                                        dispersed=self.ds['mass_dispersed'][y_trajectory_temp, x_time_temp])
            # 油的model
            # TODO:[*] 19-09-19 注意self.ds['density']对数组进行索引是一个masked_array
            # 有可能是masked的，所以需要判断
            oil_temp = model.OilModel(
                density=self.ds['density'][y_trajectory_temp, x_time_temp] if self.ds['density'][
                                                                                  y_trajectory_temp, x_time_temp].mask == True else None,
                film_thickness=self.ds['oil_film_thickness'][y_trajectory_temp, x_time_temp] if
                self.ds['oil_film_thickness'][
                    y_trajectory_temp, x_time_temp].mask == True else None)

            wt_temp = self.ds['sea_water_temperature'][y_trajectory_temp, x_time_temp] if \
                self.ds['sea_water_temperature'][
                    y_trajectory_temp, x_time_temp].mask == True else None
            water_fraction = self.ds['water_fraction'][y_trajectory_temp, x_time_temp] if self.ds['water_fraction'][
                                                                                              y_trajectory_temp, x_time_temp].mask == True else None
            # TODO:[*] 19-09-19 此处的思路 若出现--的这种情况，直接跳过，不用save了
            # 若为np.nan 的话直接跳过，不处理
            if (wt_temp == np.nan) is False:
                oil_model = model.OilSpillingModel(time=time_temp, point=point_temp, current=current_temp,
                                                   wind=wind_temp, status=status_temp, code=code,
                                                   wt=wt_temp, mass=mass_temp, water_fraction=water_fraction,
                                                   oil=oil_temp)
                try:
                    oil_model.save()
                except Exception as err:
                    print(f'保存 oil_model 出现异常，出现异常位置[x:{x_time_temp},y:{y_trajectory_temp}]')

            # y_index = y_index + 1
        # 对当前的时间对应的所有点进行平均
        # 0-24
        wind_temp = model.WindModel(x=self.ds['x_wind'][:].T[x_time_temp].mean(),
                                    y=self.ds['y_wind'][:].T[x_time_temp].mean())
        current_temp = model.CurrentModel(x=self.ds['x_sea_water_velocity'][:].T[x_time_temp].mean(),
                                          y=self.ds['x_sea_water_velocity'][:].T[x_time_temp].mean())
        point_temp = [round(self.ds['lon'][:].T[x_time_temp].mean().item(), 4),
                      round(self.ds['lat'][:].T[x_time_temp].mean().item(), 4)]
        time_temp = self.get_time_data[x_time_temp]
        status_temp = self.ds['status'][:].T[x_time_temp].mean()
        # 质量model
        mass_temp = model.MassModel(oil=self.ds['mass_oil'][:].T[x_time_temp].mean(),
                                    evaporated=self.ds['mass_evaporated'][:].T[x_time_temp].mean(),
                                    dispersed=self.ds['mass_dispersed'][:].T[x_time_temp].mean())
        # 油的model
        oil_temp = model.OilModel(density=self.ds['density'][:].T[x_time_temp].mean(),
                                  film_thickness=self.ds['oil_film_thickness'][:].T[x_time_temp].mean())

        wt_temp = self.ds['sea_water_temperature'][:].T[x_time_temp].mean()
        water_fraction = self.ds['water_fraction'][:].T[x_time_temp].mean()
        oil_avg_model = model.OilspillingAvgModel(time=time_temp, point=point_temp, current=current_temp,
                                                  wind=wind_temp, status=status_temp, code=code,
                                                  wt=wt_temp, mass=mass_temp, water_fraction=water_fraction,
                                                  oil=oil_temp)
        try:
            oil_avg_model.save()
        except Exception as err:
            print(f'保存avg出现异常，出现异常位置[x:{x_time_temp},y:{y_trajectory_temp}]')

        print(f'[-] 当前处理第:{x_time_temp},共:{self.get_x_time - 1}')

    def circulation(self, code: str):
        '''
            循环写入
        :return:
        '''
        x_index = 0
        y_index = 0
        # TODO:[*] 19-09-19 此处改为使用多进程
        with concurrent.futures.ThreadPoolExecutor(max_workers=setting._MAX_WORKERS) as executor:
            to_do = []
            for x_time_temp in range(self.get_x_time - 1 if setting._DEBUG else 1):
                future = executor.submit(self.circulation_trajectory, x_time_temp, code)
                to_do.append(future)
            for future in concurrent.futures.as_completed(to_do):
                future.result()
        # for x_time_temp in range(self.get_x_time - 1):
        # 0-2xxx
        # 将下面代码封装至 def circulation_trajectory 中
        # for y_trajectory_temp in range(self.get_y_trajectory - 1):
        #     # 0-73
        #     wind_temp = model.WindModel(x=self.ds['x_wind'][y_trajectory_temp, x_time_temp],
        #                                 y=self.ds['y_wind'][y_trajectory_temp, x_time_temp])
        #     current_temp = model.CurrentModel(x=self.ds['x_sea_water_velocity'][y_trajectory_temp, x_time_temp],
        #                                       y=self.ds['x_sea_water_velocity'][y_trajectory_temp, x_time_temp])
        #     # point = [all_data['lon'][i], all_data['lat'][i]]
        #     point_temp = [round(self.ds['lon'][y_trajectory_temp, x_time_temp].item(), 6),
        #                   round(self.ds['lat'][y_trajectory_temp, x_time_temp].item(), 6)]
        #     time_temp = self.get_time_data[x_time_temp]
        #     status_temp = self.ds['status'][y_trajectory_temp, x_time_temp]
        #     # 质量model
        #     mass_temp = model.MassModel(oil=self.ds['mass_oil'][y_trajectory_temp, x_time_temp],
        #                                 evaporated=self.ds['mass_evaporated'][y_trajectory_temp, x_time_temp],
        #                                 dispersed=self.ds['mass_dispersed'][y_trajectory_temp, x_time_temp])
        #     # 油的model
        #     # TODO:[*] 19-09-19 注意self.ds['density']对数组进行索引是一个masked_array
        #     # 有可能是masked的，所以需要判断
        #     oil_temp = model.OilModel(
        #         density=self.ds['density'][y_trajectory_temp, x_time_temp] if self.ds['density'][
        #                                                                           y_trajectory_temp, x_time_temp].mask == True else None,
        #         film_thickness=self.ds['oil_film_thickness'][y_trajectory_temp, x_time_temp] if self.ds['oil_film_thickness'][
        #                                                                           y_trajectory_temp, x_time_temp].mask == True else None)
        #
        #     wt_temp = self.ds['sea_water_temperature'][y_trajectory_temp, x_time_temp] if self.ds['sea_water_temperature'][
        #                                                                           y_trajectory_temp, x_time_temp].mask == True else None
        #     water_fraction = self.ds['water_fraction'][y_trajectory_temp, x_time_temp] if self.ds['water_fraction'][
        #                                                                           y_trajectory_temp, x_time_temp].mask == True else None
        #     # TODO:[*] 19-09-19 此处的思路 若出现--的这种情况，直接跳过，不用save了
        #     # 若为np.nan 的话直接跳过，不处理
        #     if (wt_temp==np.nan) is False:
        #         oil_model = model.OilSpillingModel(time=time_temp, point=point_temp, current=current_temp,
        #                                            wind=wind_temp, status=status_temp, code=code,
        #                                            wt=wt_temp, mass=mass_temp, water_fraction=water_fraction,
        #                                            oil=oil_temp)
        #         try:
        #             oil_model.save()
        #         except Exception as err:
        #             print(f'保存 oil_model 出现异常，出现异常位置[x:{x_time_temp},y:{y_trajectory_temp}]')
        #
        #     y_index = y_index + 1
        # # 对当前的时间对应的所有点进行平均
        # # 0-24
        # wind_temp = model.WindModel(x=self.ds['x_wind'][:].T[x_time_temp].mean(),
        #                             y=self.ds['y_wind'][:].T[x_time_temp].mean())
        # current_temp = model.CurrentModel(x=self.ds['x_sea_water_velocity'][:].T[x_time_temp].mean(),
        #                                   y=self.ds['x_sea_water_velocity'][:].T[x_time_temp].mean())
        # point_temp = [round(self.ds['lon'][:].T[x_time_temp].mean().item(), 4),
        #               round(self.ds['lat'][:].T[x_time_temp].mean().item(), 4)]
        # time_temp = self.get_time_data[x_time_temp]
        # status_temp = self.ds['status'][:].T[x_time_temp].mean()
        # # 质量model
        # mass_temp = model.MassModel(oil=self.ds['mass_oil'][:].T[x_time_temp].mean(),
        #                             evaporated=self.ds['mass_evaporated'][:].T[x_time_temp].mean(),
        #                             dispersed=self.ds['mass_dispersed'][:].T[x_time_temp].mean())
        # # 油的model
        # oil_temp = model.OilModel(density=self.ds['density'][:].T[x_time_temp].mean(),
        #                           film_thickness=self.ds['oil_film_thickness'][:].T[x_time_temp].mean())
        #
        # wt_temp = self.ds['sea_water_temperature'][:].T[x_time_temp].mean()
        # water_fraction = self.ds['water_fraction'][:].T[x_time_temp].mean()
        # oil_avg_model = model.OilspillingAvgModel(time=time_temp, point=point_temp, current=current_temp,
        #                                           wind=wind_temp, status=status_temp, code=code,
        #                                           wt=wt_temp, mass=mass_temp, water_fraction=water_fraction,
        #                                           oil=oil_temp)
        # try:
        #     oil_avg_model.save()
        # except Exception as err:
        #     print(f'保存avg出现异常，出现异常位置[x:{x_time_temp},y:{y_trajectory_temp}]')
        #
        # print(f'[-] 当前处理第:{x_time_temp},共:{self.get_x_time - 1}')

        x_index = x_index + 1
        pass


from .common import DataType


class DataFactory:
    '''
        data 工厂方法 ，用于对上面的 两类 data 对象进行解耦
    '''
    switch = {
        DataType.Oil_Spilling: OilSpillingData,
        DataType.Search_Rescue: SearchRescueData
    }

    factory = None

    def _build_data(self, type: DataType):
        '''
            根据传入的 type 返回对应的 data class
        :param type:
        :return:
        '''
        self.factory = self.switch[type]

    def __init__(self, type: DataType):
        if self.factory is None:
            self._build_data(type)

    def run(self, dir_path: str, file_name: str):
        if self.factory is not None:
            data_temp = self.factory(dir_path, file_name)
            data_temp.init()
            data_temp.insert2DB()
