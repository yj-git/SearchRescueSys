from datetime import datetime
from util.enum import TaskStateEnum, JobTypeEnum


class JobInfoMidModel:
    '''
        对应 User_JobInfo表+User_JobUserRate表中的一些关键信息组成的中间实体
    '''

    def __init__(self, date: datetime, name: str, state: int, area: int, tag: str, rate: int, code: str):
        self.date = date
        self.name = name
        self.state = state
        self.area = area
        self.tag = tag
        self.rate = rate
        self.code = code


class JobMidModel:
    '''

    '''

    def __init__(self, case_code: str, area: int, job_type: JobTypeEnum = JobTypeEnum.OIL, attrs: {} = None):
        self.case_code = case_code
        self.area = area
        self._job_type = job_type if job_type is not None else JobTypeEnum.OIL
        # self._job_type = job_type
        self._attrs: {} = attrs

    @property
    def attrs(self) -> {}:
        return self._attrs

    @property
    def job_type_val(self):
        return self._job_type.value

    @attrs.setter
    def attrs(self, attrs_new: {}):
        if self._attrs is not None:
            self._attrs.update(attrs_new)
        else:
            self._attrs = attrs_new

    @property
    def wind_id(self):
        return self._attrs.get('wind_id')

    @wind_id.setter
    def wind_id(self, wind_id: int):
        self._attrs['wind_id'] = wind_id

    @property
    def current_id(self):
        return self._attrs.get('current_id')

    @current_id.setter
    def current_id(self, current_id: int):
        self._attrs['current_id'] = current_id


class CaseNumsMidModel:
    def __init__(self, date: datetime, nums: int):
        self.date = date
        self.nums = nums
