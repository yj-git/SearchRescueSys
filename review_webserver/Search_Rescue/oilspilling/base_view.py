import os
from util.user import get_user

class OilBaseView:
    def get_mearn(self, factor: str, uid: int, **kwargs):
        '''
            流程：
                -1 根据uid判断指定user是否存在(可复用)
                -2 根据 auth_user->user_jobuserrate->user_jobinfo 找到对应的路径(现数据库中还缺少相关字段)
                -3 读取指定指定路径下的文件
                -4 文件验证(此部分未实现——可先跳过)
                -5 读取文件
                -6 读取传入的 factor的均值(注意不同的factor有不同的阈值范围)
        :param factor:
        :return:
        '''
        # 找到当前factor的阈值范围
        max = kwargs['max']
        min = kwargs['min']
        target_user = get_user(uid)
        if target_user is not None:
            # TODO:[*] 20-01-16 此部分为模拟
            # 现直接获取到文件路径
            root_path = r''
            file_name = ''
            full_name = os.path.join(root_path, file_name)

        pass
