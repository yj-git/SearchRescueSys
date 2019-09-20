from rest_framework import serializers
from .models import *
from apps.rescue.serializers import CurrentModelSerializer, WindModelSerializer


class MassModelSerializer(serializers.Serializer):
    '''
       质量相关model
    '''
    # 溢油的质量
    oil = serializers.FloatField()
    # 蒸发的质量
    evaporated = serializers.FloatField()
    # 分散的质量
    dispersed = serializers.FloatField()


class OilModelSerializer(serializers.Serializer):
    '''
        油相关的model
    '''
    # 油的密度
    density = serializers.FloatField()
    # 油膜的厚度
    film_thickness = serializers.FloatField()


class OilSpillingModelSerializer(serializers.Serializer):
    '''
        溢油基础model
    '''
    code = serializers.CharField()
    status = serializers.IntegerField()
    time = serializers.DateTimeField()
    point = PointField()
    current = CurrentModelSerializer()
    wind = WindModelSerializer()
    # 海温
    wt = serializers.FloatField()
    mass = MassModelSerializer()
    # 水含量
    water_fraction = serializers.FloatField()

    oil = OilModelSerializer()


class OilspillingAvgModelSerializer(serializers.Serializer):
    '''
        溢油平均值model
    '''
    code = serializers.CharField()
    status = serializers.IntegerField()
    time = serializers.DateTimeField()
    point = PointField()
    current = CurrentModelSerializer()
    wind = WindModelSerializer()
    # 海温
    wt = serializers.FloatField()
    mass = MassModelSerializer()
    # 水含量
    water_fraction = serializers.FloatField()

    oil = OilModelSerializer()
