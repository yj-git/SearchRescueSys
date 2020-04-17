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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from conf.settings import _MYSQL, DOWNLOAD_ROOT, GEO_CURRENT_ROOT, GEO_WIND_ROOT, _WORK_SPACE
from model.models import DictBase, GeoCoverageinfo, GeoLayerinfo, GeoStoreinfo, GeoWorkspaceinfo, UserTaskinfo, RelaGeoBase

class DbFile:
    def __init__(self, host, db_name, user, password):
        self.host = host
        self.db_name = db_name
        self.user = user
        self.password = password
        #self.engine = create_engine("mysql+pymysql://root:admin123@localhost/searchrescue", encoding='utf-8', echo=True)
        self.engine = create_engine(("mysql+pymysql://%s:%s@%s/%s" % (user, password, host, db_name)), encoding='utf-8', echo=True)

    def record_state(self, file_name, target_dir):
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
        userTaskInfo.create_date = datetime.now()
        userTaskInfo.forecast_date = datetime.now().date()
        userTaskInfo.ext = 'nc'
        userTaskInfo.state = 2
        fileCode = file_name.split('_')
        if (len(fileCode) > 2):
            if (fileCode[1] == 'cur'):
                userTaskInfo.coverage_type = session.query(DictBase).filter_by(type_code='CURRENT').first().code
                userTaskInfo.coverage_area = session.query(DictBase).filter_by(type_code=fileCode[0]).first().code
            elif (fileCode[1] == 'wrf'):
                userTaskInfo.coverage_type = session.query(DictBase).filter_by(type_code='WIND').first().code
                userTaskInfo.coverage_area = session.query(DictBase).filter_by(type_code='nwp').first().code
            session.add(userTaskInfo)

        # 记录GeoCoverageinfo状态
        geoCoverageinfo = GeoCoverageinfo()
        fileCode = file_name.split('_')
        if (fileCode[1] == 'cur'):
            geoCoverageinfo.root_path = GEO_CURRENT_ROOT
        elif (fileCode[1] == 'wrf'):
            geoCoverageinfo.root_path = GEO_WIND_ROOT
        geoCoverageinfo.relative_path = os.path.join(str(datetime.now().date().year),
                                                     str(datetime.now().date().month), str(datetime.now().date().day))
        geoCoverageinfo.file_name = file_name
        file_size = os.path.getsize(os.path.join(target_dir, file_name))
        geoCoverageinfo.file_size = file_size
        geoCoverageinfo.create_date = datetime.now()
        if (len(fileCode) > 2):
            if (fileCode[1] == 'cur'):
                geoCoverageinfo.coverage_type = session.query(DictBase).filter_by(type_code='CURRENT').first().code
                geoCoverageinfo.coverage_area = session.query(DictBase).filter_by(type_code=fileCode[0]).first().code
            elif (fileCode[1] == 'wrf'):
                geoCoverageinfo.coverage_type = session.query(DictBase).filter_by(type_code='WIND').first().code
                geoCoverageinfo.coverage_area = session.query(DictBase).filter_by(type_code='nwp').first().code
            session.add(geoCoverageinfo)

        # 记录geoStoreinfo状态
        geoStoreinfo = GeoStoreinfo()
        fileCode = file_name.split('_')
        if (fileCode[1] == 'cur'):
            geoStoreinfo.work_space = _WORK_SPACE.get('CURRENT')
        elif (fileCode[1] == 'wrf'):
            geoStoreinfo.work_space = _WORK_SPACE.get('WIND')
        geoStoreinfo.store_name = file_name[:(len(file_name) - 3)]
        geoStoreinfo.store_type = 301
        session.add(geoStoreinfo)
        session.commit()

