#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/7 10:23
# @Author  : evaseemefly
# @Desc    : 所有的job与定时任务相关均放在此处
# @Site    : 
# @File    : job.py
# @Software: PyCharm
from datetime import datetime
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.mongodb import MongoDBJobStore

from conf.settings import _MONGO

mongo_client = MongoClient(_MONGO.get('HOST'), _MONGO.get('PORT'))

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


# 以下定义的为各类job
# TODO:[-] 20-04-07 + 所有的job的命名规范为: 所属事务_类型_job
@scheduler.scheduled_job('cron', id="coverage_current_job", hour=8, minute=30, jobstore='mongo')
def coverage_current_job():
    '''
        通过cron表达式定义的负责条件的定时器
    :return:
    '''
    print(f'执行每日定时任务:coverage_current_job|now:{datetime.now()}')
    # 下面再调用 -> ftp.py ->


def coverage_wind_job():
    '''
        TODO:[*] 20-04-07 by cwb
    :return:
    '''
    pass
