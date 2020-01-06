from rest_framework.decorators import APIView
from rest_framework.response import Response
# Create your views here.
import dateutil

# 本项目的
from .models import OilspillingAvgModel, OilSpillingModel
from .middle_model import StartEndDateMidModel
from .serializers import OilspillingAvgModelSerializer, OilSpillingModelSerializer, StartEndDateMidModelSerializer

# 新加入的延时的任务
from apps.oilspilling.tasks.tasks import my_task


class OilSpillingTrackAvgView(APIView):
    def get(self, request):
        '''
            根据code获取该code的溢油随着时间的平均轨迹点
        :param request:
        :return:
        '''
        code = request.GET.get('code', None)
        track_list = []
        if code is not None:
            track_list = OilspillingAvgModel.objects(code=code)
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
            oil_track_list = OilSpillingModel.objects(code=code, time=target_date_dt)
        json_data = OilSpillingModelSerializer(oil_track_list, many=True).data
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
            real_data = OilspillingAvgModel.objects(code=code, time=target_data_dt)
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
            real_data = OilspillingAvgModel.objects(code=code, time=target_date_dt)
        json_data = OilspillingAvgModelSerializer(real_data[0], many=False).data
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
            list_avg = OilspillingAvgModel.objects(code=code).distinct(field='time')
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
        Response('未提供code')


class CreateOilSpillingView(APIView):
    def post(self, request):
        my_task.delay('测试测试')
        pass
        return Response()
