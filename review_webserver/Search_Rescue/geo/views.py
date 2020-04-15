from typing import List

from django.shortcuts import render
from rest_framework.decorators import APIView, api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from geoserver.catalog import Catalog
from util.common import DEFAULT_FK
from util.enum import TaskStateEnum
from geo.models import CoverageModel
from geo.serializers import CoverageSerializer
from users.view_base import TaskBaseView
from users.models import TaskUserModel
from base.view_base import CoverageBaseView

# Create your views here.

cat = Catalog("http://localhost:8083/geoserver/rest")


class CoverageInfoView(TaskBaseView):
    '''
        TODO:[*] 此处出现问题:
            TypeError: Cannot create a consistent method resolution
                    order (MRO) for bases APIView, CoverageBaseView
    '''

    def get(self, request):
        # coverage_type_str: str = request.GET.get('type', None)
        # coverage_area_str: str = request.GET.get('area', None)
        # coverage_type: int = int(coverage_type_str) if coverage_type_str is not None else DEFAULT_FK
        # coverage_area: int = int(coverage_area_str) if coverage_area_str is not None else DEFAULT_FK
        coverage_type, coverage_area = self.covert_request_typearea(request)
        # TODO:[-] 20-04-15 此处需要先从 -> user_taskinfo 表中找到对应的记录 -> coverage_id 再根据 coverage_id 找到 -> geo_coverageinfo 表中的记录，
        # 并做验证
        list_task: List[TaskUserModel] = self.get_task_coverage(request)
        match_list: List[CoverageModel] = []
        for temp_task in list_task:
            match_list.extend(CoverageModel.objects.filter(id=temp_task.coverage_id).all())
        json_data = CoverageSerializer(match_list, many=True).data
        return Response(json_data)
