#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/1 16:50
# @Author  : evaseemefly
# @Desc    :
# @Site    : 
# @File    : settings.py
# @Software: PyCharm

_FTP = {
    '_URL': '128.5.6.142',
    '_USERNAME': 'Currents',
    '_PWD': '123'
}
# 增加风场FTP地址，caiwb 2020-04-13
_FTP_WIND = {
    '_URL': '128.5.6.142',
    '_USERNAME': 'wind',
    '_PWD': '123'
}
# 用来存储 ftp 下载的文件的根目录(或放在数据库中？)
# DOWNLOAD_ROOT = r'D:\01proj\SearchRescueSys\data\download'
# DOWNLOAD_ROOT = r'd:\data\SearchRescueSys\data\download'  #caiwb 2020-04-13
DOWNLOAD_ROOT = r'/Users/evaseemefly/Documents/03Data/nc'


# 用来存储要发布的nc文件
GEO_CURRENT_ROOT = r'D:\03data\geoserver_data\current'
GEO_WIND_ROOT = r'D:\setup\GeoServer\GeoServer 2.13.0\data_dir\nmefc\waterwind'

# work_space相关设置
_WORK_SPACE = {
    'CURRENT': 'nmefc_current',
    'WIND': 'nmefc_wind'
}

# mongo相关的配置
_MONGO = {
    'COLLECTION': 'geo_job',
    'DB_NAME': 'test',
    'HOST': '127.0.0.1',
    'PORT': 27017
}

_MYSQL = {
    'DB_NAME': 'searchrescue',
    'HOST': '127.0.0.1',
    'USER': 'root',
    'PASSWORD': '123456',
}

COVERAGE_STORE={
    ''
}