#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/8 11:07 上午
# @Author  : evaseemefly
# @Desc    :
# @Site    : 
# @File    : middle_model.py
# @Software: PyCharm
from typing import List


class TaskMsg:
    def __init__(self, attrs: {} = {}):
        self._attrs = attrs

    @property
    def attrs(self):
        return self._attrs

    @attrs.setter
    def attrs(self, val):
        self._attrs = val

    @property
    def celery_id(self):
        return self._attrs.get('job_celery_id', None)

    @celery_id.setter
    def celery_id(self, val):
        self._attrs['job_celery_id'] = val

    @property
    def case_code(self):
        return self._attrs.get('case_code', None)

    @case_code.setter
    def case_code(self, val):
        self._attrs['case_code'] = val

    @property
    def area(self):
        return self._attrs.get('area', None)

    @area.setter
    def area(self, val):
        self._attrs['area'] = val

    @property
    def rate(self):
        return self._attrs.get('rate', None)

    @rate.setter
    def rate(self, val):
        self._attrs['rate'] = val

    @property
    def state(self):
        return self._attrs.get('state', None)

    @state.setter
    def state(self, val):
        self._attrs['state'] = val

    @property
    def type_job(self):
        return self._attrs.get('type_job', None)

    @type_job.setter
    def type_job(self, val):
        self._attrs['type_job'] = val

    @property
    def uid(self):
        return self._attrs.get('uid', None)

    @uid.setter
    def uid(self, val):
        self._attrs['uid'] = val

    @property
    def start_time(self):
        return self._attrs.get('start_time', None)

    @start_time.setter
    def start_time(self, val):
        self._attrs['start_time'] = val

    @property
    def end_time(self):
        return self._attrs.get('end_time', None)

    @end_time.setter
    def end_time(self, val):
        self._attrs['end_time'] = val

    @property
    def jid(self):
        '''
            user_jobinfo 表中的 -> id
        :return:
        :rtype:
        '''
        return self._attrs.get('jid', None)

    @jid.setter
    def jid(self, val):
        self._attrs['jid'] = val

    @property
    def wind_id(self):
        '''
            对应的是 geo_coverageinfo 表
        :return:
        :rtype:
        '''
        return self._attrs.get('wind_id', None)

    @wind_id.setter
    def wind_id(self, val):
        self._attrs['wind_id'] = val

    @property
    def current_id(self):
        '''
            对应的是 geo_coverageinfo 表
        :return:
        :rtype:
        '''
        return self._attrs.get('current_id', None)

    @current_id.setter
    def current_id(self, val):
        self._attrs['current_id'] = val

    @property
    def nc_files(self) -> List[str]:
        '''
            对应的是 geo_coverageinfo 表
        :return:
        :rtype:
        '''
        return self._attrs.get('nc_files', [])

    @nc_files.setter
    def nc_files(self, val: List[str]):
        self._attrs['nc_files'] = val
