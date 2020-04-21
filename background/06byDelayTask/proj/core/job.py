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
from abc import ABCMeta, abstractmethod
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.mongodb import MongoDBJobStore

from typing import List
# 当前项目
from conf.settings import _MONGO, DOWNLOAD_ROOT, _FTP, _FTP_WIND
from core.file import IFileBase, ICoverageFile, CurrentCoverageFile, WindCoverageFile
from core.ftp import FtpFactory
from core.data import CurrentCoverage4NC, ICoverage4NC
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
    # list_products.append(ProductMidModel(ProductType.CURRENT, [AreaNameMidModel(Area.BOHAISEA, f'bhs_cur_{re_str}.nc'),
    #                                                             AreaNameMidModel(Area.EASTCHINASEA,
    #                                                                                    f'ecsnew_current_{re_str}.nc'),
    #                                                            AreaNameMidModel(Area.INDIAN, f'ind_cur_{re_str}.nc'),
    #                                                             AreaNameMidModel(Area.SOUTHCHINASEA,
    #                                                                             f'scs_cur_{re_str}.nc'),
    #                                                            AreaNameMidModel(Area.NORTHWEST,
    #                                                                             f'nwp_cur_{re_str}.nc')],
    #                                      os.path.join(DOWNLOAD_ROOT, 'current')))
    # TODO:[-] 20-04-20 演示时只测试 东中国海的数据
    list_products.append(ProductMidModel(ProductType.CURRENT, [
        AreaNameMidModel(Area.EASTCHINASEA,
                         f'ecsnew_current_{re_str}.nc')],
                                         os.path.join(DOWNLOAD_ROOT, 'current')))
    # 风场
    # TODO:[-] 20-04-14 增加风场预报时效 by caiwb
    list_products.append(ProductMidModel(ProductType.WIND, [AreaNameMidModel(Area.NORTHWEST, f'nmefc_wrf_{re_str}00.nc')
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
            # TODO:[*] 20-04-09 由于在 -> init_product 中 的 AreaNameMidModel -> re 实际就是对应的文件名称(目前的需求是每天不同区域的风场或流场的数据只有一个——实效)
            current_file = CurrentCoverageFile('', DOWNLOAD_ROOT, temp_area.re, datetime.now(), temp_area.re)
            ftp.batch_download(current_file)
            # 转换
            current_covert_wf: ICoverageWorkFlow = CurrentCoverageWorkFlow(datetime.now(), current_file.save_path)
            current_covert_wf.init_convert(current_file.file_name)
            pass


# TODO:[*] 20-04-07 需要加入一个记录 定时任务 的表


@scheduler.scheduled_job('cron', id="coverage_wind_job", hour=8, minute=30, jobstore='mongo')
def coverage_wind_job():
    '''
        通过cron表达式定义的负责条件的定时器
        TODO:[*] 20-04-07 by cwb
    :return:
    '''
    print(f'执行每日定时任务:coverage_wind_job|now:{datetime.now()}')
    # 下面再调用 -> ftp.py -> batch_download 批量下载
    # 次数需要根据当前时间创建一个 IFileBase 的实现类
    ftp = FtpFactory(_FTP_WIND.get('_URL'), _FTP_WIND.get('_USERNAME'), _FTP_WIND.get('_PWD'))
    product_wind = [prodcut_wind for prodcut_wind in list_products if
                    prodcut_wind.product_type == ProductType.WIND]
    for wind_area in product_wind[0].area_names:
        if len(product_wind) == 1:
            wind_file = WindCoverageFile('', DOWNLOAD_ROOT, wind_area.re, datetime.now())
            ftp.batch_download(wind_file)
    pass


class ICoverageWorkFlow(metaclass=ABCMeta):
    '''
        抽象的 栅格数据的工作流 抽象类，部分方法需要子类实现
    '''

    def __init__(self, current: datetime, root_path: str):
        '''
            current: 当前时间
            areas:   所有的区域 middle model
        :param current:
        :param root_path:
        '''
        self.current = current
        self.root_path = root_path
        self.areas: List[AreaNameMidModel] = []

    @abstractmethod
    def coverage_convert(self, *args, **kwargs):
        pass

    def init_convert(self, file_name: str):
        '''
            执行转换的主方法，调用需要子类实现的 -> coverage_convert 方法
        :param root_path:
        :param file_name:
        :return:
        '''
        self.coverage_convert(file_name=file_name)


class CurrentCoverageWorkFlow(ICoverageWorkFlow):
    '''
        流场的 工作流
    '''

    def coverage_convert(self, *args, **kwargs):
        '''
            大体流程:
                1- 读取指定文件
                2- 数据验证
                3- 修改指定的 variables -> u/v -> 修改 long_name ，添加 standard_name
        :param args:
        :param kwargs:
        :return:
        '''
        # 存储路径 + 名称
        root_path = self.root_path
        file_name = kwargs.get('file_name')

        coverage_nc: ICoverage4NC = CurrentCoverage4NC(root_path, file_name, ['lat', 'lon', 'time'], ['u', 'v'])
        coverage_nc.init_modify()

        pass
