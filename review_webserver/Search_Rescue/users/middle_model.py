from datetime import datetime


class JobInfoMidModel:
    '''
        对应 User_JobInfo表+User_JobUserRate表中的一些关键信息组成的中间实体
    '''

    def __init__(self, date: datetime, name: str, state: int, area: int, tag: str, rate: int):
        self.date = date
        self.name = name
        self.state = state
        self.area = area
        self.tag = tag
        self.rate = rate


class CaseNumsMidModel:
    def __init__(self, date: datetime, nums: int):
        self.date = date
        self.nums = nums
