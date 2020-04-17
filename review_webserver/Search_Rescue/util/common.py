# 包含部分通用的方法
from datetime import datetime
import os
# from apps.user.models import AuthUserDir, CaseInfo
from Search_Rescue.settings import _ROOT_DIR

ROOT_PATH = _ROOT_DIR

DEFAULT_FK = -1
DEFAULT_NULL_KEY = -1


def get_path(temp: str, dt: datetime):
    '''
        根据传入的时间与temp(一般为user_id）合成最终的路径 xx/temp/yyyy/mm
    :param dt:
    :return:
    '''
    return os.path.join(ROOT_PATH, temp, dt.strftime('%Y'), dt.strftime('%m'))

#
# def check_case_name(user_id: str, case_name: str) -> bool:
#     '''
#         根据指定user_id判断指定user_id是否已经创建了指定case_name
#     :param user_id:
#     :param case_name:
#     :return:
#     '''
#     # TODO:[*] 20-02-04 引发了一个错误，暂时去掉
#     users = User.objects.filter(id=user_id)
#     if len(users) > 0:
#         # 获取该用户的全部的case
#         rela_user_case: List[AuthUserDir] = AuthUserDir.objects.filter(uid=users[0].id)
#         case_names: List[str] = []
#         if len(rela_user_case) > 0:
#             # 获取所有的CaseInfo
#             case_names = [CaseInfo.objects.filter(id=temp.did.id)[0].case_name for temp in rela_user_case]
#         # 判断传入的case_name 是否存在在user的关系中
#         if case_name in case_names:
#             return True
#         return False
#     pass
