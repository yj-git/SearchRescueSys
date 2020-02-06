from rest_framework import serializers
from .models import *
from apps.rescue.serializers import CurrentModelSerializer, WindModelSerializer
# TODO:[*] 20-01-07 引入drf的mongoengine的序列化对象
from rest_framework_mongoengine import serializers as drf_serializers


# import rest_framework_mongoengine


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


class OilModelSerializerByEngine(drf_serializers.EmbeddedDocumentSerializer):
    '''
        油相关的model
    '''

    # 油的密度
    # density = drf_serializers.DocumentSerializer.FloatField()
    # # 油膜的厚度
    # film_thickness = drf_serializers.DocumentSerializer.FloatField

    class Meta:
        model = OilModel
        fields = '__all__'


class OilSpillingTrackModelSerializer(serializers.Serializer):
    '''
        溢油轨迹model 序列化器
    '''
    # code = serializers.CharField()
    status = serializers.IntegerField()
    # time = serializers.DateTimeField()
    point = serializers.DictField()


class OilSpillingModelSerializer(serializers.Serializer):
    '''
        溢油基础model
    '''
    code = serializers.CharField()
    status = serializers.IntegerField()
    time = serializers.DateTimeField()
    point = serializers.DictField()
    # 海温
    wt = serializers.FloatField()
    # 水含量
    water_fraction = serializers.FloatField()

    oil = OilModelSerializer()
    current = CurrentModelSerializer()
    wind = WindModelSerializer()
    mass = MassModelSerializer()


# TODO:[*] 20-01-08 使用serializers.ModelSerializer序列化mongoengine的model时会出错，暂时不要使用此种方式
# class OilSpillingModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OilSpillingModel
#         fields = ['code', 'status']


# TODO:[*] 20-01-08 尝试集成serializers.ModelSerializer，不再使用serializers.Serializer

class OilSpillingModelSerializerByEngine(drf_serializers.DocumentSerializer):
    '''
        溢油基础model
    '''

    class Meta:
        model = OilSpillingModel
        fields = '__all__'
        # fields = ('code', 'status')
    # code = drf_serializers.StringField()
    # status = drf_serializers.IntegerField()
    # time = drf_serializers.DateTimeField()
    # point = drf_serializers.DictField()
    # current = CurrentModelSerializer()
    # wind = WindModelSerializer()
    # # 海温
    # wt = serializers.FloatField()
    # mass = MassModelSerializer()
    # 水含量
    # water_fraction = drf_serializers.FloatField()

    # oil = OilModelSerializerByEngine()
class OilspillingAvgModelSerializer_bak(serializers.Serializer):
    '''
        溢油平均值model
    '''
    code = serializers.CharField()
    status = serializers.IntegerField()
    time = serializers.DateTimeField()
    point = serializers.DictField()
    current = CurrentModelSerializer()
    wind = WindModelSerializer()
    # 海温
    wt = serializers.FloatField()
    mass = MassModelSerializer()
    # 水含量
    water_fraction = serializers.FloatField()

class OilspillingAvgModelSerializer(serializers.Serializer):
    '''
        溢油平均值model
    '''
    code = serializers.CharField()
    status = serializers.IntegerField()
    time = serializers.DateTimeField()
    point = serializers.DictField()
    x_sea_water_velocity=serializers.FloatField()
    y_sea_water_velocity=serializers.FloatField()
    x_wind=serializers.FloatField()
    y_wind=serializers.FloatField()
    mass_oil=serializers.FloatField()
    mass_evaporated=serializers.FloatField()
    mass_dispersed=serializers.FloatField()
    oil_film_thickness=serializers.FloatField()
    density=serializers.FloatField()
    sea_water_temperature=serializers.FloatField()
    # current = CurrentModelSerializer()
    # wind = WindModelSerializer()

    # 海温
    # wt = serializers.FloatField()
    # mass = MassModelSerializer()
    # 水含量
    water_fraction = serializers.FloatField()


class StartEndDateMidModelSerializer(serializers.Serializer):
    '''
        对应 apps/oilspilling/middle_model.py 中的 StartEndDateMidModel
    '''
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
