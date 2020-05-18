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
from typing import List
from rest_framework.request import Request
from .enum import TaskStateEnum, JobTypeEnum
from users.models import JobInfo, JobUserRate
from rela.views_base import RelaCaseOilView
from base.middle_model import TaskMsg
from util.customer_exception import LackNeedSubmitFactorsError


def provide_job_rate(rate: int, state: TaskStateEnum, job_type=JobTypeEnum, jid: int = None):
    '''
        修改provide的装饰器
        只是用来向 user_jobuserrate 这张进度表中插入进度相关信息的
    '''

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwrags):
        # params_attrs: {} = kwrags.get('attrs', None)
        # TODO:[-] 20-05-08 此处修改为使用 TaskMsg
        task_msg: TaskMsg = kwrags.get('task_msg', None)
        if state == TaskStateEnum.RUNNING and rate == 0:
            # 只创建 jobinfo
            now = datetime.utcnow()
            # attrs: {} = kwrags.get('attrs', None)
            JobInfo.objects.create(type=job_type, case_code=task_msg.case_code, gmt_create=now,
                                   gmt_modified=now,
                                   is_del=False, area=task_msg.area)
        elif rate != 0:
            # 此处为更新 user_jobuserrate
            JobUserRate.objects.create(rate=rate, state=state.value, gmt_create=datetime.utcnow(),
                                       gmt_modified=datetime.utcnow(), jid_id=task_msg.jid,
                                       uid_id=task_msg.uid)
            pass

        return wrapped(*args, **kwrags)

    return wrapper


def request_need_factors_wrapper(need_factors: List[str], method_type: str = 'GET'):
    '''
        判断是否所需要的要素全部包含在request中
    :param need_factors:
    :return:
    '''

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        request: Request = args[0]
        if all([temp_need in getattr(request,method_type) for temp_need in need_factors]):
            return wrapped(*args, **kwargs)
        else:
            raise LackNeedSubmitFactorsError(f'lack needs in :{need_factors}')

    # request = kwargs.get('request')
    return wrapper
