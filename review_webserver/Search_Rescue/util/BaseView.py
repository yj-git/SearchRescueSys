from rest_framework.decorators import APIView
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,


)

class BaseView(APIView):
    '''
        普通用户
    '''
    permission_classes = (
        IsAuthenticated
    )

class SuperUserpermissions(APIView):
    '''
        管理员用户
    '''
    permission_classes = (IsAdminUser,)

class NotLogin(APIView):
    pass