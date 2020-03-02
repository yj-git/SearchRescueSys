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
from rest_framework.pagination import PageNumberPagination
# rest_framework_mongoengine  相关
from rest_framework_mongoengine import viewsets as drf_viewsets
# 本项目的配置
from Search_Rescue.settings import PAGINATION
# 本项目的
from .models import OilspillingAvgModel, OilSpillingModel
from .middle_model import StartEndDateMidModel
from .serializers import OilspillingAvgModelSerializer, OilSpillingModelSerializer, StartEndDateMidModelSerializer, \
    OilSpillingModelSerializerByEngine, OilSpillingTrackModelSerializer

# 新加入的延时的任务
# from apps.oilspilling.tasks.tasks import my_task
from tasks.tasks import my_task
# from .tasks.oil_task import do_job
from oilspilling.tasks.oil_task import do_job
from util.reader import OilFileReader, create_reader
from oilspilling.base_view import OilBaseView
from util.enum import JobTypeEnum
from util.guide import Guide

# 7530
_ROOT_DIR = r'D:\02proj\SearchRescue\SearchRescueSys\data\demo_data'
# 5820
# _ROOT_DIR = r'D:\02proj\new_SearchRescueSys\SearchRescueSys\data\demo_data'
# 5510
# _ROOT_DIR = r'C:\01Proj\SearchRescueSys\data\demo_data'
# p52s
# _ROOT_DIR = r'D:\03data\oil'

_RESULT_FILE = 'sanjioil.nc'

TYPE_EM = 'dev'


def FULL_PATH():
    import os
    if TYPE_EM == 'dev':
        return os.path.join(_ROOT_DIR, _RESULT_FILE)
    else:
        return ''


class LargeResultsSetPagination(PageNumberPagination):
    '''
        提取散点用的分页类
    '''
    page_size = 400
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 1000


class OilSpillingTrackCountView(APIView, OilBaseView):
    def get(self, request):
        '''
            获取指定时间的散点总数
        :param request:
        :return:
        '''
        target_date_str = request.GET.get('date', None)
        code = request.GET.get('code', None)
        target_date = dateutil.parser.parse(target_date_str)
        if None in [target_date_str, code]:
            return Response()
        else:
            reader_func = create_reader('file')
            # TODO:[-] 20-03-02 此处需要修改路径为动态加载，并封装至 OilBaseView 中
            # guide = Guide(JobTypeEnum.OIL)
            # root_path, relative_path = guide.get_pathes(code)
            root_path, relative_path = self.get_nc_paths(code)
            reader = reader_func(root_path, relative_path)
            count = 0
            try:
                count = reader.read_track_count(target_date)
            except OSError:
                print(f'不存在指定文件')
            return Response(count)


class OilSpillingTrackAvgView(APIView):
    '''
        获取指定code对应的全部散点的时间平均轨迹
    '''
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
        msg = ''
        if code is not None:
            try:
                # track_list = OilspillingAvgModel.objects(code=code)
                # TODO:[*] 20-02-03 此处需要修改当请求进来
                reader_cls = create_reader('db')
                # 实例化
                reader = reader_cls(_ROOT_DIR, _RESULT_FILE)
                # TODO:[-] 20-02-06 注意此处传入的code为 mongo中的code(实际db中对应的job_name)
                track_list = reader.read_avg_track(code)
            except KeyError:
                msg = '不存在的key索引/时间超出范围'
            except Exception as e:
                msg = f'其他错误:{e}'

        # TODO:[*] 20-01-17 此处注意一下，由于重新修改了序列化的原始data model 改为了mid model，mid model中缺少部分需要序列化的字段，序列化时会提示有错误，注意！
        json_data = OilspillingAvgModelSerializer(track_list, many=True).data
        return Response(json_data)

    def get_track_db(self, request):
        '''
            通过读取db的方式读取平均溢油轨迹
        :param request:
        :return:
        '''


class OilSpillingTrackView(APIView, OilBaseView):
    # 设定提取指定时间的散点用的分页类(一次性提取3000个散点对后台压力有些大)
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        '''
            根据指定的 date 获取该date的 所有溢油点
            TODO:[*] 20-01-06 此处准备重写 若重写的话，不将oil对应的数据入库，数据库中只记录文件所在路径，直接读取文件获取对应的信息
        :param request:
        :return:
        '''
        # TODO:[*] 20-01-20 最新的设计想通过分批加载的方式解决加载较慢的问题
        target_date_str = request.GET.get('date')
        code = request.GET.get('code', None)
        page_index = int(request.GET.get('pageindex', PAGINATION['DEFAULT_INDEX']))
        page_count = int(request.GET.get('pagecount', PAGINATION['DEFAULT_COUNT']))
        target_date_dt = dateutil.parser.parse(target_date_str)
        oil_track_list = []
        json_data = None
        msg = 'no error'
        if code is not None:
            try:
                reader_func = create_reader('file')
                root_path, relative_path = self.get_nc_paths(code)
                reader = reader_func(root_path, relative_path)
                oil_track_list = reader.read_current_track(code, target_date_str, page_index=page_index,
                                                           page_count=page_count)

                # oil_track_list = OilSpillingModel.objects(
                #     code=code, time=target_date_dt)
                json_data = OilSpillingTrackModelSerializer(oil_track_list, many=True).data
            except KeyError:
                msg = '不存在的key索引/时间超出范围'
            except:
                msg = '其他错误'
        # return Response(
        #     {
        #         'data': json_data,
        #         'error': msg
        #     }
        # )
        return Response(json_data)
        # return Response(msg if json_data is None else json_data)


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
        json_data = None
        msg = ''
        if code is not None:
            try:
                real_data = OilspillingAvgModel.objects(
                    code=code, time=target_data_dt)
                json_data = OilspillingAvgModelSerializer(real_data[0]).data
            except KeyError:
                msg = '不存在的key索引/时间超出范围'
            except Exception as e:
                msg = '其他错误'
                print(e)

        return Response(msg if json_data is None else json_data)


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


class OilSpillingTrackAvgDateRangeView(APIView, OilBaseView):
    def get(self, request):
        '''
            根据指定 code 获取对应code对应的平均观测值的日期数组
        :param request:
        :return:
        '''
        code = request.GET.get('code', None)
        list_avg = []
        if code is not None:
            # 修改为直接从mongo中读取
            reader_func = create_reader('db')
            # TDOO:[*] 20-03-02 注意此处使用的是写死的 路径，此处需要修改为从数据库中读取的方式
            # 注意此处需要通过 app user 根据case_code查找对应的model
            self.get_target_file_path(code)
            reader = reader_func(_ROOT_DIR, _RESULT_FILE)
            try:

                list_avg = reader.read_date_range(code=code, type=JobTypeEnum.OIL)

                # TODO:[-] 20-01-21 不再使用数据库的读取这种方式，放在OilDbReader中
                # 根据time去重
                # list_avg = OilspillingAvgModel.objects(
                #     code=code).distinct(field='time')
                # if len(list_avg) > 0:
                #     list_avg = list(set(list_avg))
                #     # 排序
                #     list_avg.sort()
                temp = StartEndDateMidModel(list_avg[0], list_avg[-1])

                return Response(StartEndDateMidModelSerializer(temp).data)
            except IOError:
                return Response('不存在指定文件', status=500)
            except IndexError:
                # list_avg 长度为0
                return Response('不存在指定的code的记录', status=500)
        # return Response()
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
    # permission_classes = (IsAuthenticated,)
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


class DoPyJobView(APIView):
    def get(self, request):
        # 直接调用tasks
        # TODO:[*] 20-02-06 此处只是执行提交操作，读取不在此处处理
        do_job()
        return Response('写入成功')
