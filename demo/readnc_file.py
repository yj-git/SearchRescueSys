from netCDF4 import Dataset as ncfile
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

path = 'E:\\project\\oilspill_rescue\\rescue\\output\\'

nc_file = ncfile(path + 'qz_ty1_100p.nc', 'r')
# print(nc_file)
lon_list = nc_file.variables['lon']             # 读取NC文件中的变量
lat_list = nc_file.variables['lat']
lon = np.array(lon_list)                        # 转成数组
lat = np.array(lat_list)
# lon_0 = lon_list[0, :]                               # 读取数组第1行的所有列
# lon_0[lon_0 > 360] = np.nan                     # 数组中大于360的数据都赋值NAN
# lon_mean = np.nanmean(lon_0)                    # 求数组中除NAN外数据的平均值


lon_mean = []
lat_mean = []
for i in range(len(lon[0, :])):

    lon_temp = lon[:, i]
    lat_temp = lat[:, i]

    lon_temp[lon_temp > 360] = np.nan
    lat_temp[lat_temp > 360] = np.nan

    lon_temp_mean = np.nanmean(lon_temp)
    lat_temp_mean = np.nanmean(lat_temp)

    lon_mean.append(lon_temp_mean)
    lat_mean.append(lat_temp_mean)

m = Basemap(projection='cyl', resolution='h', llcrnrlon=118.8, llcrnrlat=24.7,urcrnrlon=119.2, urcrnrlat=24.9)

m.drawcoastlines()  # 画岸线

m.fillcontinents(color='#DFF0D8', lake_color='aqua')
m.drawmapboundary(fill_color='#D9EDF7')

m.drawparallels(np.arange(24.7, 24.9, 0.05), labels=[1,0,0,0])
m.drawmeridians(np.arange(118.8, 119.2, 0.1), labels=[0,0,0,1])
#
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False   #用来正常显示负号
#
m.plot(lon_mean, lat_mean, 'bo-', linewidth=2, markersize=3, label=u'轨迹')
m.plot(lon_mean[0], lat_mean[0], 'r^', markersize=6, label=u'初始位置')
plt.legend(loc='upper left')
plt.show()

