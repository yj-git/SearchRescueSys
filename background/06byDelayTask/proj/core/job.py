#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/7 10:23
# @Author  : evaseemefly
# @Desc    : 所有的job与定时任务相关均放在此处
# @Site    : 
# @File    : job.py
# @Software: PyCharm
import os
from datetime import datetime
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.mongodb import MongoDBJobStore

from typing import List

from conf.settings import _MONGO, DOWNLOAD_ROOT, _FTP
from core.file import IFileBase, ICoverageFile, CurrentCoverageFile
from core.ftp import FtpFactory
from model.midemodel import AreaNameMidModel, ProductMidModel
from common.enum import Area, ProductType

mongo_client = MongoClient(_MONGO.get('HOST'), _MONGO.get('PORT'))

DOWNLOAD_ROOT = DOWNLOAD_ROOT

SCHEDULER_JOB_STORES = {
    'mongo': MongoDBJobStore(collection=_MONGO.get('COLLECTION'), database=_MONGO.get('DB_NAME'), client=mongo_client),
    'default': MemoryJobStore()
}

scheduler = BlockingScheduler(jobstores=SCHEDULER_JOB_STORES)


def scheduler_start():
    '''
        启动 作业任务调度器
    :return:
    '''
    scheduler.start()


list_products: List[ProductMidModel] = []


def init_product(current: datetime):
    '''
        初始化 product
    :return:
    '''
    # 获取当前时间的匹配的str
    re_str = f'{current.strftime("%Y%m%d")}'

    # 流场
    list_products.append(ProductMidModel(ProductType.CURRENT, [AreaNameMidModel(Area.BOHAISEA, f'bhs_cur_{re_str}.nc'),
                                                               AreaNameMidModel(Area.EASTCHINASEA,
                                                                                f'ecs_new_current_{re_str}.nc'),
                                                               AreaNameMidModel(Area.INDIAN, f'ind_cur_{re_str}.nc'),
                                                               AreaNameMidModel(Area.SOUTHCHINASEA,
                                                                                f'scs_cur_{re_str}.nc'),
                                                               AreaNameMidModel(Area.NORTHWEST,
                                                                                f'nwp_cur_{re_str}.nc')],
                                         os.path.join(DOWNLOAD_ROOT, 'current')))
    # 风场
    list_products.append(ProductMidModel(ProductType.WIND, [AreaNameMidModel(Area.NORTHWEST, f'nmefc_wrf_{re_str}.nc')
                                                            ],
                                         os.path.join(DOWNLOAD_ROOT, 'wind')))


# 以下定义的为各类job
# TODO:[-] 20-04-07 + 所有的job的命名规范为: 所属事务_类型_job
@scheduler.scheduled_job('cron', id="coverage_current_job", hour=8, minute=30, jobstore='mongo')
def coverage_current_job():
    '''
        通过cron表达式定义的负责条件的定时器
    :return:
    '''
    print(f'执行每日定时任务:coverage_current_job|now:{datetime.now()}')
    # 下面再调用 -> ftp.py -> batch_download 批量下载
    # 次数需要根据当前时间创建一个 IFileBase 的实现类
    # TODO:[*] 20-04-07 可以去掉 url 以及 file_name

    ftp = FtpFactory(_FTP.get('_URL'), _FTP.get('_USERNAME'), _FTP.get('_PWD'))
    product_current = [prodcut_temp for prodcut_temp in list_products if
                       prodcut_temp.product_type == ProductType.CURRENT]
    if len(product_current) == 1:
        for temp_area in product_current[0].area_names:
            current_file = CurrentCoverageFile('', DOWNLOAD_ROOT, '', datetime.now(), temp_area.re)
            ftp.batch_download(current_file)
            pass


# TODO:[*] 20-04-07 需要加入一个记录 定时任务 的表


def coverage_wind_job():
    '''
        TODO:[*] 20-04-07 by cwb
    :return:
    '''
    pass