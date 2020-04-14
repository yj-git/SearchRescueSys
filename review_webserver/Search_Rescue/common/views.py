from django.shortcuts import render

from rest_framework.decorators import APIView, api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import generics
# 尝试引入类型约束
from typing import List

from common.models import SelectModel
from common.serializers import SelectModelSerializer
from common.view_base import IBaseSelectListView


class SelectListView(APIView, IBaseSelectListView):

    def get(self, request):
        parent, type_select = self.get_base_params(request)
        # type_str: str = request.GET.get('type', None)
        # parent_str: int = request.GET.get('parent', None)
        # parent: int = 0 if parent_str is None else int(parent_str)
        # type: int = 0 if type_str is None else int(type_str)
        children: List[SelectModel] = []
        if type_select:
            # 1- 找到母菜单
            parents: List[SelectModel] = SelectModel.objects.filter(parent=parent, type_select=type_select)
            # 2- 判断母菜单是否包含子菜单
            children = SelectModel.objects.filter(parent=parents[0].id)
        json_data = SelectModelSerializer(children, many=True).data
        return Response(json_data)


class SelectParentListView(APIView, IBaseSelectListView):
    '''
        父级菜单集合
    '''

    def get(self, request):
        '''

        '''
        parent, type_select = self.get_base_params(request)
        parents: List[SelectModel] = []
        if type_select:
            # 1- 找到母菜单
            parents: List[SelectModel] = SelectModel.objects.filter(parent=parent, type_select=type_select)
            # 2- 判断母菜单是否包含子菜单
            # children = SelectModel.objects.filter(parent=parents[0].id)
        json_data = SelectModelSerializer(parents, many=True).data
        return Response(json_data)


class SelectComplexListView(APIView):
    def get(self, request):
        '''
            获取复杂菜单(带级联的菜单)
        '''
        pass
