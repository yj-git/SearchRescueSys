from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import CurrentModel, SearchRescueModel, WindModel
from .serializers import SearchRescueModelSerializer, SimpleValMidModelSerializer,SimpleDirValMidModelSerializer
from .middle_model import SimpleValMidModel,SimpleDirValMidModel


# Create your views here.

class RescueTrackView(APIView):
    def get(self, request):
        '''
            获取搜救模型的轨迹信息
        :param request:
        :return:
        '''
        # 根据code去查询
        code = request.GET.get('code', None)
        rescue_list = []
        if code is not None:
            rescue_list = SearchRescueModel.objects(code=code)
        json_data = SearchRescueModelSerializer(rescue_list, many=True).data
        return Response(json_data)


class FactorListView(APIView):
    def get(self, request):
        '''
            根据要素获取该要素的观测值
            v1版本：由于wind与current是嵌套的所以对于这两个应该特别对待
        :param request:
        :return:
        '''
        code = request.GET.get('code', None)
        factor = request.GET.get('factor', None)
        factor_list = []
        if None not in [code, factor]:
            # factor_list=SearchRescueModel.objects(code=code).values(factor)
            factor_list = SearchRescueModel.objects(code=code).only(factor)
            # json_data = SearchRescueModelSerializer(factor_list, many=True).data
            if factor in ['wind','current']:
                filter_list =[SimpleDirValMidModel(val=temp[factor]) for temp in factor_list]
                json_data=SimpleDirValMidModelSerializer(filter_list,many=True).data
            elif factor not in['wind','current']:
                filter_list=[SimpleValMidModel(val=temp[factor]) for temp in factor_list]
                json_data=SimpleValMidModelSerializer(filter_list,many=True).data
        #

        return Response(json_data)
