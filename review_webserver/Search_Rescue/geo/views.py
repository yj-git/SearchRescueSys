from typing import List

from django.shortcuts import render
from rest_framework.decorators import APIView, api_view, authentication_classes, permission_classes
from rest_framework.response import Response
import arrow
from datetime import datetime
# from geoserver.catalog import Catalog
from util.common import DEFAULT_FK, DEFAULT_NULL_KEY
from util.enum import TaskStateEnum
from util.customer_wrapt import request_need_factors_wrapper
from geo.models import CoverageModel, RGeoInfo, GeoLayerModel, GeoServerBaseModel
from geo.serializers import CoverageSerializer, LayerSerializer, GeoserverSerializer
from users.view_base import TaskBaseView
from users.models import TaskUserModel
from base.view_base import CoverageBaseView
from .views_base import CoverageBaseView as GeoBaseView


# Create your views here.

# cat = Catalog("http://localhost:8083/geoserver/rest")


class CoverageListView(TaskBaseView):
    '''

        TODO:[*] 此处出现问题:
            TypeError: Cannot create a consistent method resolution
                    order (MRO) for bases APIView, CoverageBaseView
    '''

    def get(self, request):
        '''
             根据 type , area 获取对应的 coverageinfo 数据(list)
        :param request:
        :type request:
        :return:List[coverageinfo]
        :rtype:
        '''
        # TODO:[-] 20-04-15 此处需要先从 -> user_taskinfo 表中找到对应的记录 -> coverage_id 再根据 coverage_id 找到 -> geo_coverageinfo 表中的记录，
        # 并做验证
        list_task: List[TaskUserModel] = self.get_task_coverage(request)
        match_list: List[CoverageModel] = []
        for temp_task in list_task:
            # user_taskinfo -> rela_geobase.coverage_id -> geo_coverageinfo
            match_list.extend([rela_temp.coverage for rela_temp in RGeoInfo.objects.filter(task_id=temp_task.id).all()])
            # match_list.extend(CoverageModel.objects.filter(id=temp_task.coverage_id).all())
        json_data = CoverageSerializer(match_list, many=True).data
        return Response(json_data)


class GeoInfoView(TaskBaseView):
    def get(self, request):
        '''
            获取 geo_layerinfo 这张表对应的数据(list)
        :param request:
        :return: List[GeoLayerModel]
        '''
        task_id_str: str = request.GET.get('taskid', None)
        list_task: List[TaskUserModel] = TaskUserModel.objects.filter(
            id=int(task_id_str) if task_id_str is not None else DEFAULT_NULL_KEY).all()
        match_list: List[GeoLayerModel] = []
        for temp_task in list_task:
            # user_taskinfo -> rela_geobase.coverage_id -> geo_coverageinfo
            match_list.extend([rela_temp.layer for rela_temp in RGeoInfo.objects.filter(task_id=temp_task.id).all()])
            # match_list.extend(CoverageModel.objects.filter(id=temp_task.coverage_id).all())
        json_data = LayerSerializer(match_list, many=True).data
        return Response(json_data)


class CoverageFileListView(APIView, GeoBaseView):
    '''
        20-05-17 新加入的根据传入的 datetime 获取指定时间范围内的所有 coverage files 列表
    '''

    @request_need_factors_wrapper(['current'], 'GET')
    def get(self, request):
        current_str: str = request.GET.get('current')
        current_dt = arrow.get(current_str)
        start, end = self.get_datetime_range(current_dt)
        coverage_list = CoverageModel.objects.filter(gmt_forecast_start__gt=start.datetime,
                                                     gmt_forecast_start__lte=end.datetime)
        json_data = CoverageSerializer(coverage_list, many=True).data
        return Response(json_data)
        pass


class GeoServerView(APIView):
    '''
        geoserver 的服务列表
    '''

    def get(self, request):
        '''
            获取 geoserver 的服务列表
        :param request:
        :type request:
        :return:
        :rtype:
        '''
        list: List[GeoServerBaseModel] = GeoServerBaseModel.objects.all()
        json_data = GeoserverSerializer(list, many=True).data
        return Response(json_data)
