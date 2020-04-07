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

# 用来存储 ftp 下载的文件的根目录(或放在数据库中？)
DOWNLOAD_ROOT = r'D:\01proj\SearchRescueSys\data\download'

# mongo相关的配置
_MONGO = {
    'COLLECTION': 'geo_job',
    'DB_NAME': 'test',
    'HOST': '127.0.0.1',
    'PORT': 27017
}
