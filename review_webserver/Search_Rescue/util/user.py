from django.contrib.auth.models import User


def get_user(uid: int):
    '''
        根据 uid 找到对应的user
    :param uid:
    :return:
    '''
    users = User.objects.filter(id=uid)
    if len(users) > 0:
        # 取出第一个
        return users[0]
    return None
