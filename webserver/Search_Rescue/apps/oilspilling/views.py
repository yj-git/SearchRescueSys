import sys
from datetime import datetime
from rest_framework.decorators import APIView
from rest_framework.response import Response
# Create your views here.
import dateutil

# 引入drf的权限认证
from rest_framework import permissions

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
# TODO:[*] 引入jwt的token认证
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication

# rest_framework_mongoengine  相关
from rest_framework_mongoengine import viewsets as drf_viewsets
# 本项目的
from .models import OilspillingAvgModel, OilSpillingModel
from .middle_model import StartEndDateMidModel
from .serializers import OilspillingAvgModelSerializer, OilSpillingModelSerializer, StartEndDateMidModelSerializer, \
    OilSpillingModelSerializerByEngine, OilSpillingTrackModelSerializer

# 新加入的延时的任务
from apps.oilspilling.tasks.tasks import my_task

from apps.util.reader import OilFileReader, create_reader


class OilSpillingTrackAvgView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        '''
            根据code获取该code的溢油随着时间的平均轨迹点
        :param request:
        :return:
        '''
        code = request.GET.get('code', None)
        # TODO:[-] 20-01-16 此处修改为直接读取nc文件，不读取数据库
        track_list = []
        if code is not None:
            # track_list = OilspillingAvgModel.objects(code=code)
            reader_func = create_reader('file')
            # reader = reader_func(r'D:\02proj\new_SearchRescueSys\SearchRescueSys\background\01byJupyter\data',
            #                      'sanjioil.nc')
            reader = reader_func(r'C:\01Proj\SearchRescueSys\data\demo_data',
                                 'sanjioil.nc')
            track_list = reader.read_avg_track('test')
        # TODO:[*] 20-01-17 此处注意一下，由于重新修改了序列化的原始data model 改为了mid model，mid model中缺少部分需要序列化的字段，序列化时会提示有错误，注意！
        json_data = OilspillingAvgModelSerializer(track_list, many=True).data
        return Response(json_data)
        pass


class OilSpillingTrackView(APIView):
    def get(self, request):
        '''
            根据指定的 date 获取该date的 所有溢油点
            TODO:[*] 20-01-06 此处准备重写 若重写的话，不将oil对应的数据入库，数据库中只记录文件所在路径，直接读取文件获取对应的信息
        :param request:
        :return:
        '''
        target_date_str = request.GET.get('date')
        code = request.GET.get('code', None)
        target_date_dt = dateutil.parser.parse(target_date_str)
        oil_track_list = []
        if code is not None:
            reader_func = create_reader('file')
            reader = reader_func(r'D:\02proj\SearchRescue\SearchRescueSys\data\demo_data', 'sanjioil.nc')
            # reader = reader_func(r'D:\02proj\new_SearchRescueSys\SearchRescueSys\data\demo_data',
            #                      'sanjioil.nc')
            oil_track_list = reader.read_current_track('test', target_date_str)

            # oil_track_list = OilSpillingModel.objects(
            #     code=code, time=target_date_dt)
        json_data = OilSpillingTrackModelSerializer(oil_track_list, many=True).data
        return Response(json_data)


class TargetDateRealDataView(APIView):
    '''
        获取指定 date 以及 code 对应的 OilspillingAvgModel 的值
    '''

    def get(self, request):
        '''

        :param request:
        :return:
        '''

        target_data_str = request.GET.get('date')
        code = request.GET.get('code', None)
        # 转换成date
        target_data_dt = dateutil.parser.parse(target_data_str)
        real_data = None
        if code is not None:
            real_data = OilspillingAvgModel.objects(
                code=code, time=target_data_dt)
        json_data = OilspillingAvgModelSerializer(real_data[0]).data
        return Response(json_data)


class OilRealDataAvgView(APIView):
    def get(self, request):
        '''
            根据指定 code 以及date 获取对应的点的各平均观测值
        :param request:
        :return:
        '''
        target_date_str = request.GET.get('date')
        code = request.GET.get('code', None)
        target_date_dt = dateutil.parser.parse(target_date_str)
        real_data = None
        if code is not None:
            real_data = OilspillingAvgModel.objects(
                code=code, time=target_date_dt)
        json_data = OilspillingAvgModelSerializer(
            real_data[0], many=False).data
        return Response(json_data)
        # pass


class OilSpillingTrackAvgDateRangeView(APIView):
    def get(self, request):
        '''
            根据指定 code 获取对应code对应的平均观测值的日期数组
        :param request:
        :return:
        '''
        code = request.GET.get('code', None)
        list_avg = []
        if code is not None:
            # 根据time去重
            list_avg = OilspillingAvgModel.objects(
                code=code).distinct(field='time')
            if len(list_avg) > 0:
                list_avg = list(set(list_avg))
                # 排序
                list_avg.sort()
                # for temp in list_avg:
                #     print(temp)
                # 获取起始时间及终止时间以及日期列表
                temp = StartEndDateMidModel(list_avg[0], list_avg[-1])

                return Response(StartEndDateMidModelSerializer(temp).data)
            return Response()
        return Response('未填code', status=200)


class CreateOilSpillingView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # 注意此处可以通过 request._user 获取对应的user对象
        username = ''
        if hasattr(request, '_user'):
            if hasattr(request._user, 'username'):
                name = request._user.username
                username = name
                try:

                    # 获取了用户名称之后，向celery提交耗时作业
                    my_task.delay(username)
                    pass
                    return Response('提交成功')
                except TypeError:
                    # raise ImportError('Missing redis library (pip install redis)')
                    # kombu.exceptions.OperationalError: Error 10061 connecting to localhost: 6379.由于目标计算机积极拒绝，无法连接。.
                    print("Unexpected error:", sys.exc_info()[0])
                    return Response('Unexpected error')
        return Response('提交失败')


# TODO:[*] 20-01-09 此处注释一下，不使用视图集，而使用APIView(个人觉得APIView对于请求的整个流程更好控制，Viewset还是不太熟悉)
class TokenTestView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response("请求成功")
        pass

    def post(self, request):
        # 注意此处可以通过 request._user 获取对应的user对象
        username = ''
        if hasattr(request, '_user'):
            if hasattr(request._user, 'username'):
                name = request._user.username
                username = name
                # 获取了用户名称之后，向celery提交耗时作业
                my_task.delay("")
                pass
            # username = request._user.username
        # request._user.get('username')
        return Response(username)


class TestViewset(drf_viewsets.ModelViewSet):
    # TODO:[*] 20-01-08 加入Token的认证
    # 注意此处不能使用 TokenAuthentication 的原因是 TokenAuthentication是 rest_framework.authentication的认证方式改为jwt的
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # permission_classes = (IsAuthenticated,)
    # permission_classes = [TokenAuthentication]
    # queryset = OilSpillingModel.objects(code='sanjioil', time='2018-01-14T23:20:00Z')
    # queryset = OilSpillingModel.objects(code='sanjioil', time='2018-01-14T23:20:00Z')
    # TODO:[*] 20-01-06 此处使用此序列化器会有问题
    # 不再使用rest_framework_mongoengine 提供的序列化器了
    serializer_class = OilSpillingModelSerializerByEngine

    # @action(methods=['get'], detail=False)
    def get_queryset(self):
        # TODO:[*] 此处遇见一个问题：若mongo中不存在指定数据，那么会出现目标计算机无法连接的错误
        # pymongo.errors.ServerSelectionTimeoutError: localhost:27017: [WinError 10061] 由于目标计算机积极拒绝，无法连接。
        queryset = OilSpillingModel.objects(
            code='sanjioil', time='2018-01-14T23:20:00Z')
        return queryset
    #     pass
    # def test(self, request):
    # return Response(OilSpillingModelSerializer(self.queryset).data)
