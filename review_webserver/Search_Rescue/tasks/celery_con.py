#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/22 5:22 下午
# @Author  : evaseemefly
# @Desc    :
# @Site    : 
# @File    : celery_con.py
# @Software: PyCharm
import os
from celery import Celery, platforms
from django.conf import settings
from tasks.settings import BROKER_URL, CELERY_RESULT_BACKEND, CELERY_TASK_SERIALIZER, CELERY_RESULT_SERIALIZER, \
    CELERY_TASK_RESULT_EXPIRES, CELERY_ACCEPT_CONTENT

# 为celery设置环境变量 django -> settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Search_Rescue.settings')
app = Celery(
    backend='amqp',
    broker=BROKER_URL,
    CELERY_ROUTES={
        'worker.test1': {'queue': 'test1'}
    },
)
# 允许celery以root权限启动
platforms.C_FORCE_ROOT = True
app.conf.update(
    CELERY_TASK_SERIALIZER=CELERY_TASK_SERIALIZER,
    CELERY_RESULT_SERIALIZER=CELERY_RESULT_SERIALIZER,
    CELERY_IGNORE_RESULT=True,
    CELERYD_PREFETCH_MULTIPLIER=10,
    CELERYD_MAX_TASKS_PER_CHILD=200,
)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
