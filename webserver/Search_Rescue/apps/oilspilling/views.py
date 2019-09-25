from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework import status
from rest_framework.response import Response
# Create your views here.
import dateutil

# 本项目的
from .models import OilspillingAvgModel, OilSpillingModel
from .serializers import OilspillingAvgModelSerializer, OilSpillingModelSerializer


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
