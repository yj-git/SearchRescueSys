#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/2 14:37
# @Author  : evaseemefly
# @Desc    : 操作数据库的相关操作放在此处
# @Site    : 
# @File    : db.py
# @Software: PyCharm

import os
from datetime import datetime
import xarray as xar
import netCDF4 as nc
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from conf.settings import _MYSQL, DOWNLOAD_ROOT, GEO_CURRENT_ROOT, GEO_WIND_ROOT, _WORK_SPACE
from model.models import DictBase, GeoCoverageinfo, GeoLayerinfo, GeoStoreinfo, GeoWorkspaceinfo, UserTaskinfo, \
    RelaGeoBase
from util.tools import local_to_utc, utc_to_local

class DbFile:
    def __init__(self, host:str, db_name:str, user:str, password:str):
        self.host = host
        self.db_name = db_name
        self.user = user
        self.password = password
        # self.engine = create_engine("mysql+pymysql://root:admin123@localhost/searchrescue", encoding='utf-8', echo=True)
        self.engine = create_engine(("mysql+mysqldb://%s:%s@%s/%s" % (user, password, host, db_name)), encoding='utf-8',
                                    echo=True)

    def record_state(self, file_name: str, target_dir: str):
        '''
        记录海流、海面风数值预报文件下载状态，初始化文件GeoServer的Coverage、Store基本信息
        :param target_dir:
        :param file_name:
        :return:
        '''
        Session_class = sessionmaker(bind=self.engine)
        session = Session_class()

        # 记录UserTaskinfo状态
        userTaskInfo = UserTaskinfo()
        userTaskInfo.root_path = DOWNLOAD_ROOT
        userTaskInfo.case_path = target_dir[-(len(target_dir) - len(DOWNLOAD_ROOT) - 1):]
        # TODO:[-] 20-04-19 注意往数据库里写入时是 世界时 注意！
        userTaskInfo.create_date = local_to_utc(datetime.now())
        # TODO:[-] 20-04-19 此处的预报时效有误，不应该是 当前时间，而是通过 文件名 + 种类确定
        file_path = os.path.join(target_dir, file_name)
        ds = nc.Dataset(file_path)
        ds_xr = xar.open_dataset(file_path)
        forecast_date_utc = pd.to_datetime(ds_xr.coords['time'].values[0])
        userTaskInfo.forecast_date = forecast_date_utc
        userTaskInfo.ext = 'nc'
        userTaskInfo.state = 2
        fileCode = file_name.split('_')
        area_code = fileCode[0]
        type_code = fileCode[1]
        if (len(fileCode) > 2):
            # TODO:[*] 20-04-20 建议以下部分，因为都有 判断是否 为 流 还是 风 的判断，最好写在一块，或者写成一个 私有方法
            # TODO:[-] 20-04-19 此处判断时注意 东中国海 ，ecs_new_current_xx.nc -> ecsnew_current_20200420.nc
            # if (fileCode[1] == 'cur' or (fileCode[1] == 'new' and fileCode[2] == 'current')):
            if (type_code == 'cur' or type_code == 'current'):
                userTaskInfo.coverage_type = session.query(DictBase).filter_by(type_code='CURRENT').first().code
                # TODO:[-] 20-04-20 此处会出现bug
                # err: AttributeError: 'NoneType' object has no attribute 'code'
                # 此处由于 修改了文件名称 , 现在为 ecsnew
                userTaskInfo.coverage_area = session.query(DictBase).filter_by(type_code=type_code).first().code
            elif (type_code == 'wrf'):
                userTaskInfo.coverage_type = session.query(DictBase).filter_by(type_code='WIND').first().code
                userTaskInfo.coverage_area = session.query(DictBase).filter_by(type_code='nwp').first().code
            session.add(userTaskInfo)

        # 记录GeoCoverageinfo状态
        geoCoverageinfo = GeoCoverageinfo()
        fileCode = file_name.split('_')
        if (type_code == 'cur' or type_code == 'current'):
            geoCoverageinfo.root_path = GEO_CURRENT_ROOT
        elif (type_code == 'wrf'):
            geoCoverageinfo.root_path = GEO_WIND_ROOT
        geoCoverageinfo.relative_path = os.path.join(str(datetime.now().date().year),
                                                     str(datetime.now().date().month), str(datetime.now().date().day))
        geoCoverageinfo.file_name = file_name
        file_size = os.path.getsize(os.path.join(target_dir, file_name))
        geoCoverageinfo.file_size = file_size
        geoCoverageinfo.create_date = local_to_utc(datetime.now())

        if (len(fileCode) > 2):
            if (type_code == 'cur' or type_code == 'current'):
                if (('time' in ds.dimensions) and ('lat' in ds.dimensions) and ('lon' in ds.dimensions)):
                    dims = 'time,lat,lon'
                else:
                    dims = ''
                if (('u' in ds.variables) and ('v' in ds.variables)):
                    vars = 'u,v'
                else:
                    vars = ''
                geoCoverageinfo.dimessions = dims
                geoCoverageinfo.variables = vars
                geoCoverageinfo.coverage_type = session.query(DictBase).filter_by(type_code='CURRENT').first().code
                geoCoverageinfo.coverage_area = session.query(DictBase).filter_by(type_code=area_code).first().code
            elif (type_code == 'wrf'):
                if (('time' in ds.dimensions) and ('latitude' in ds.dimensions) and ('longitude' in ds.dimensions)):
                    dims = 'time,latitude,longitude'
                else:
                    dims = ''
                if (('U10' in ds.variables) and ('V10' in ds.variables)):
                    vars = 'U10,V10'
                else:
                    vars = ''
                geoCoverageinfo.dimessions = dims
                geoCoverageinfo.variables = vars
                geoCoverageinfo.coverage_type = session.query(DictBase).filter_by(type_code='WIND').first().code
                geoCoverageinfo.coverage_area = session.query(DictBase).filter_by(type_code='nwp').first().code
            session.add(geoCoverageinfo)

        # 记录geoStoreinfo状态
        geoStoreinfo = GeoStoreinfo()
        fileCode = file_name.split('_')
        if (type_code== 'cur' or type_code == 'current'):
            geoStoreinfo.work_space = _WORK_SPACE.get('CURRENT')
        elif (type_code == 'wrf'):
            geoStoreinfo.work_space = _WORK_SPACE.get('WIND')
        geoStoreinfo.store_name = file_name[:(len(file_name) - 3)]
        geoStoreinfo.store_type = 301
        session.add(geoStoreinfo)
        session.commit()
