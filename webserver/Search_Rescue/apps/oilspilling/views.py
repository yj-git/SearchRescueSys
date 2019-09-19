from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework import status
from rest_framework.response import Response
# Create your views here.

class OilSpillingTrackAvgView(APIView):
    def get(self,request):
        '''
            根据code获取该code的溢油随着时间的平均轨迹点
        :param request:
        :return:
        '''
        code =request.GET.get('code',None)
        pass

class OilSpillingTrackView(APIView):
    def get(self,request):
        '''
            根据指定的 date 获取该date的 所有溢油点
        :param request:
        :return:
        '''
        target_date_str=request.GET.get('date')