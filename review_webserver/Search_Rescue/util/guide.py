# 本模块主要用来生成文件所在的路径
import path

from typing import List, Generic, TypeVar
from util.enum import JobTypeEnum
from users.models import CaseOilInfo, CaseRescueInfo, ICaseBaseStore
from Search_Rescue.settings import _ROOT_DIR


# T = TypeVar(ICaseBaseStore)


class Guide:
    def __init__(self, type: JobTypeEnum):
        self.type = type

    def get_pathes(self, code):
        '''
            功能描述：
                根据传入的code以及对应的job type获取对应的root path + relative path , case_code + ext
        '''
        store = None
        if self.type == JobTypeEnum.OIL:
            store = CaseOilInfo.objects.filter(case_code=code).first()
        elif self.type == JobTypeEnum.RESCUE:
            store = CaseRescueInfo.objects.filter(case_code=code).first()
        return '/'.join([_ROOT_DIR, store.root_path, store.case_path]), ''.join([store.case_code, store.ext])
