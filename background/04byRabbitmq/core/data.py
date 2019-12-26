from models import model
import pandas as pd

from core.db import my_connet

from common.common import exe_run_time

class OilSpillingData:
    # 1 先连接数据库
    my_connet()

    def __init__(self, df: pd.DataFrame, code: str):
        self.df = df
        self.code = code

    @exe_run_time
    def save_2_db(self):
        # 批量写入时先放在一个数组中
        list_data=[]
        for x_time_temp in range(len(self.df)):
            temp_data = self.df.iloc[x_time_temp]
            # 0-24
            wind_temp = model.WindModel(x=temp_data.get('x_wind'),
                                        y=temp_data.get('y_wind'))
            current_temp = model.CurrentModel(x=temp_data.get('x_sea_water_velocity'),
                                              y=temp_data.get('y_sea_water_velocity'))
            # TODO:[-] 注意使用mongoengine中的预定义的point类型，只接受python原生的float类型，不支持float32类型
            point_temp = [round(temp_data.get('lon').item(), 6),
                          round(temp_data.get('lat').item(), 6)]
            time_temp = temp_data.get('time')
            status_temp = temp_data.get('status')

            # 质量model
            mass_temp = model.MassModel(oil=temp_data.get('mass_oil'),
                                        evaporated=temp_data.get('mass_evaporated'),
                                        dispersed=temp_data.get('mass_dispersed'))
            # 油的model
            # TODO:[*] 19-09-19 注意self.ds['density']对数组进行索引是一个masked_array
            # 有可能是masked的，所以需要判断
            oil_temp = model.OilModel(
                density=temp_data.get('oil_film_thickness'),
                film_thickness=temp_data.get('density'))

            wt_temp = temp_data.get('sea_water_temperature')
            water_fraction = temp_data.get('water_fraction')

            oil_model = model.OilSpillingModel(time=time_temp, point=point_temp, current=current_temp,
                                               wind=wind_temp, status=status_temp, code=self.code,
                                               wt=wt_temp, mass=mass_temp, water_fraction=water_fraction,
                                               oil=oil_temp)

            list_data.append(oil_model)
            # oil_model.save()
            # 对当前的时间对应的所有点进行平均
            # 0-24
            # wind_temp = model.WindModel(x=self.ds['x_wind'][:].data[:].T[x_time_temp].mean(),
            #                             y=self.ds['y_wind'][:].data[:].T[x_time_temp].mean())
            # current_temp = model.CurrentModel(x=self.ds['x_sea_water_velocity'][:].data[:].T[x_time_temp].mean(),
            #                                   y=self.ds['x_sea_water_velocity'][:].data[:].T[x_time_temp].mean())
            # point_temp = [round(self.ds['lon'][:].data[:].T[x_time_temp].mean().item(), 4),
            #               round(self.ds['lat'][:].data[:].T[x_time_temp].mean().item(), 4)]
            # time_temp = self.get_time_data[x_time_temp]
            # status_temp = self.ds['status'][:].data[:].T[x_time_temp].mean()
            # search_avg_model = model.SearchRescueAvgModel(time=time_temp, point=point_temp, current=current_temp,
            #                                               wind=wind_temp, status=status_temp, code=code,
            #                                               num=str(y_trajectory_temp))
            # search_avg_model.save()
        # x_index = x_index + 1
        # TODO:[-] 19-12-26 批量写入，经对比效率提升很明显
        model.OilSpillingModel.objects.insert(list_data)
