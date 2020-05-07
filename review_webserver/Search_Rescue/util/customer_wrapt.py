#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/6 8:44 下午
# @Author  : evaseemefly
# @Desc    : 自己实现的部分装饰器
# @Site    : 
# @File    : customer_wrapt.py
# @Software: PyCharm
from datetime import datetime
import wrapt
from .enum import TaskStateEnum, JobTypeEnum
from users.models import JobInfo, JobUserRate
from rela.views_base import RelaCaseOilView


def provide_job_rate(rate: int, state: TaskStateEnum, job_type=JobTypeEnum, jid: int = None):
    '''
        修改provide的装饰器
        只是用来向 user_jobuserrate 这张进度表中插入进度相关信息的
    '''

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwrags):
        params_attrs: {} = kwrags.get('attrs')
        if state == TaskStateEnum.RUNNING and rate == 0:
            # 只创建 jobinfo
            now = datetime.utcnow()
            attrs: {} = kwrags.get('attrs', None)
            JobInfo.objects.create(type=job_type, case_code=attrs.get('case_code'), gmt_create=now, gmt_modified=now,
                                   is_del=False, area=attrs.get('area'))
        elif rate != 0:
            # 此处为更新 user_jobuserrate
            JobUserRate.objects.create(rate=rate, state=state.value, gmt_create=datetime.utcnow(),
                                       gmt_modified=datetime.utcnow(), jid_id=params_attrs.get('jid'),
                                       uid_id=params_attrs.get('uid'))
            pass

        return wrapped(*args, **kwrags)

    return wrapper
