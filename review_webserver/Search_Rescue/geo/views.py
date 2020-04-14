from typing import List

from django.shortcuts import render
from rest_framework.decorators import APIView, api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from geoserver.catalog import Catalog
from util.common import DEFAULT_FK
from geo.models import CoverageModel

# Create your views here.

cat = Catalog("http://localhost:8083/geoserver/rest")


class CoverageInfoView(APIView):
    def get(self, request):
        coverage_type_str: str = request.GET.get('type', None)
        coverage_area_str: str = request.GET.get('area', None)
        coverage_type: int = int(coverage_type_str) if coverage_type_str is not None else DEFAULT_FK
        coverage_area: int = int(coverage_area_str) if coverage_area_str is not None else DEFAULT_FK
        match_list: List[CoverageModel] = CoverageModel.objects.filter(coverage_area=coverage_area,
                                                                       coverage_type=coverage_type, is_del=False).all()

        pass
