from django.shortcuts import render

from rest_framework.decorators import APIView, api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import generics
# 尝试引入类型约束
from typing import List

from common.models import SelectModel, DictBaseModel
from common.serializers import SelectModelSerializer
from common.view_base import IBaseSelectListView
from util.common import DEFAULT_FK


class SelectListView(APIView, IBaseSelectListView):

    # TODO:[-] 20-04-14 暂时注释掉，若引发其他bug可以复原
    # def get(self, request):
    #     parent, type_select = self.get_base_params(request)
    #     # type_str: str = request.GET.get('type', None)
    #     # parent_str: int = request.GET.get('parent', None)
    #     # parent: int = 0 if parent_str is None else int(parent_str)
    #     # type: int = 0 if type_str is None else int(type_str)
    #     children: List[SelectModel] = []
    #     if type_select:
    #         # 1- 找到母菜单
    #         parents: List[SelectModel] = SelectModel.objects.filter(parent=parent, type_select=type_select)
    #         # 2- 判断母菜单是否包含子菜单
    #         children = SelectModel.objects.filter(parent=parents[0].id)
    #     json_data = SelectModelSerializer(children, many=True).data
    #     return Response(json_data)

    def get(self, request):
        '''
            TODO:[*] 此处需要修改 type_select 是否需要改为 dict 中的key？
            根据 parent 与 type_select 获取对应的菜单
        Args:
            request ():

        Returns:

        '''
        parent, type_select = self.get_base_params(request)
        parents: List[SelectModel] = []
        if type_select:
            # 1- 找到母菜单
            parents: List[SelectModel] = SelectModel.objects.filter(parent=parent, type_select=type_select).all()
            # 2- 判断母菜单是否包含子菜单
            # children = SelectModel.objects.filter(parent=parents[0].id)
        json_data = SelectModelSerializer(parents, many=True).data
        return Response(json_data)

class SelectParentListView(APIView, IBaseSelectListView):
    '''
        父级菜单集合
    '''

    def get(self, request):
        '''
            根据传入的 dict_id 从 tb:dict_base -> tb:common_select 中 common_select.did_id==dict_base.code
        Args:
            request ():

        Returns:

        '''
        parent, type_select = self.get_base_params(request)
        dict_id_str = request.GET.get('dict', None)
        dict_id = DEFAULT_FK if dict_id_str is None else int(dict_id_str)
        parents: List[SelectModel] = []
        # TODO:[-] 20-04-14 此处作为备份
        # # 1- 找到母菜单
        # parents: List[SelectModel] = SelectModel.objects.filter(parent=parent, type_select=type_select)
        # # 2- 判断母菜单是否包含子菜单
        # # children = SelectModel.objects.filter(parent=parents[0].id)
        # TODO:[*] 20-04-14 修改为新的模式
        '''
            传入的 type_select 或 一个新的字段 dict_id 为 did_id
            -> dict_base -> code == did_id
            -> 判断是否有子节点，加载子节点        
            -> 根据 dict_base :list -> common_select 表中找到 in did_id 的记录         
        '''
        dicts: List[DictBaseModel] = DictBaseModel.objects.filter(code=dict_id)
        childern: List[DictBaseModel] = []
        match_list: List[SelectModel] = []
        if len(dicts) > 0:
            for dict_temp in dicts:
                # 判断是否包含子节点
                childern.extend(list(DictBaseModel.objects.filter(pid=dict_temp.code)))
        # 遍历 children -> common_select -> child.code ===did_id
        match_list = SelectModel.objects.filter(did__code__in=[temp.code for temp in childern])
        # if type_select:
        json_data = SelectModelSerializer(match_list, many=True).data
        return Response(json_data)

# class SelectTypeListView(APIView,IBaseSelectListView):


class SelectComplexListView(APIView):
    def get(self, request):
        '''
            获取复杂菜单(带级联的菜单)
        '''
        pass
