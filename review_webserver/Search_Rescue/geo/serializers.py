#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/14 21:06
# @Author  : evaseemefly
# @Desc    :
# @Site    : 
# @File    : serializers.py
# @Software: PyCharm
from rest_framework import serializers

class CoverageSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    # 维度数组 只存维度的 名称
    dimessions = serializers.CharField()
    # 特征变量数组
    variables = serializers.CharField()
    is_original = serializers.BooleanField()
    coverage_type = serializers.IntegerField()
    coverage_area = serializers.IntegerField()
    create_date = serializers.DateTimeField()
    # 存储根目录
    root_path = serializers.CharField()
    # 存储的相对路径
    relative_path = serializers.CharField()
    # 文件名
    file_name = serializers.CharField()
    # 文件大小
    file_size = serializers.FloatField()