from typing import List

from django.shortcuts import render
from rest_framework.decorators import APIView, api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from geoserver.catalog import Catalog
from util.common import DEFAULT_FK, DEFAULT_NULL_KEY
from util.enum import TaskStateEnum
from geo.models import CoverageModel, RGeoInfo, GeoLayerModel, GeoServerBaseModel
from geo.serializers import CoverageSerializer, LayerSerializer, GeoserverSerializer
from users.view_base import TaskBaseView
from users.models import TaskUserModel
from base.view_base import CoverageBaseView

# Create your views here.

cat = Catalog("http://localhost:8083/geoserver/rest")


class CoverageListView(TaskBaseView):
    '''
        TODO:[*] 此处出现问题:
            TypeError: Cannot create a consistent method resolution
                    order (MRO) for bases APIView, CoverageBaseView
    '''

    def get(self, request):
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
            获取 geo_layerinfo 这张表对应的数据
        :param request:
        :return:
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


class GeoServerView(APIView):
    '''
        geoserver 的服务列表
    '''

    def get(self, request):
        '''

        :param request:
        :return:
        '''
        list: List[GeoServerBaseModel] = GeoServerBaseModel.objects.all()
        json_data = GeoserverSerializer(list, many=True).data
        return Response(json_data)
