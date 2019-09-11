from rest_framework import serializers
from .models import *


class CurrentModelSerializer(serializers.Serializer):
    '''
        海流
    '''
    x = serializers.FloatField()
    y = serializers.FloatField()


class WindModelSerializer(serializers.Serializer):
    '''
        风
    '''
    x = serializers.FloatField()
    y = serializers.FloatField()


class SearchRescueModelSerializer(serializers.Serializer):
    '''
        搜救数据
    '''
    code = serializers.CharField()
    status = serializers.IntegerField()
    time = serializers.DateTimeField()
    point = serializers.DictField()
    current = WindModelSerializer()
    wind = CurrentModelSerializer()
    num=serializers.CharField()


class SimpleValMidModelSerializer(serializers.Serializer):
    val = serializers.FloatField()


class XyMidModelSerializer(serializers.Serializer):
    x = serializers.FloatField()
    y = serializers.FloatField()


class SimpleDirValMidModelSerializer(serializers.Serializer):
    val = XyMidModelSerializer()
