from django.db import models
from django.utils.timezone import now
# 本项目的
from users.models import IIsDelModel, IArea
from common.models import IIdModel, IDescModel
from base.models import CHOICE_GEO_TYPE, IIsDelModel
from users.models import TaskUserModel
from util.common import DEFAULT_NULL_KEY, DEFAULT_FK


# Create your models here.

class IStoreModel(models.Model):
    # 存储根目录
    root_path = models.CharField(max_length=100)
    # 存储的相对路径
    relative_path = models.CharField(max_length=100)
    # 文件名
    file_name = models.CharField(max_length=50)
    # 文件大小
    file_size = models.FloatField(default=0.0)

    class Meta:
        abstract = True


class IEnabledModel(models.Model):
    enabled = models.BooleanField(default=True)

    class Meta:
        abstract = True


class IForecastModel(models.Model):
    # 时间
    create_date = models.DateTimeField(default=now)

    class Meta:
        abstract = True


class IGeoWorkSpaceModel(models.Model):
    work_space = models.CharField(default='default', max_length=50)
    work_space_url = models.CharField(default='default', max_length=100)

    class Meta:
        abstract = True


class GeoWorkSpaceModel(IGeoWorkSpaceModel, IIsDelModel, IEnabledModel):
    class Meta:
        db_table = 'geo_workspaceinfo'


class IGeoStoreModel(models.Model):
    work_space = models.CharField(default='default', max_length=50)
    store_name = models.CharField(default='default', max_length=100)
    store_type = models.IntegerField(choices=CHOICE_GEO_TYPE, default=DEFAULT_NULL_KEY)

    class Meta:
        abstract = True


class GeoStoreModel(IGeoStoreModel, IIsDelModel, IEnabledModel):
    class Meta:
        db_table = 'geo_storeinfo'


class ILayerModel(models.Model):
    '''
        TODO:[*] 20-04-15 加入的需要发布到geoserver的相关信息
    '''
    work_space = models.CharField(default='default', max_length=50)
    title = models.CharField(default='default', max_length=100)
    store_name = models.CharField(default='default', max_length=100)
    layer_name = models.CharField(default='default', max_length=50)

    class Meta:
        abstract = True


class GeoLayerModel(ILayerModel, IEnabledModel, IIsDelModel):
    class Meta:
        db_table = 'geo_layerinfo'


class RGeoInfo(models.Model):
    '''
        与 geoserver 相关的表的关联表
    '''
    layer = models.ForeignKey(GeoLayerModel, on_delete=models.SET_DEFAULT, default=DEFAULT_FK)
    ws = models.ForeignKey(GeoWorkSpaceModel, on_delete=models.SET_DEFAULT, default=DEFAULT_FK)
    store = models.ForeignKey(GeoStoreModel, on_delete=models.SET_DEFAULT, default=DEFAULT_FK)
    task = models.ForeignKey(TaskUserModel, on_delete=models.SET_DEFAULT, default=DEFAULT_FK)

    class Meta:
        db_table = 'rela_geo_base'


class ICoverageModel(models.Model):
    '''
        所有的栅格文件的父类
    '''
    # CHOISE_TYPE=(
    #     (0,'')
    # )
    # 维度数组 只存维度的 名称
    dimessions = models.CharField(default='', max_length=500)
    # 特征变量数组
    variables = models.CharField(default='', max_length=500)
    is_original = models.BooleanField(default=True)
    coverage_type = models.IntegerField(default=-1)
    coverage_area = models.IntegerField(default=-1)

    class Meta:
        abstract = True


class CoverageModel(IIdModel, IIsDelModel, IStoreModel, IForecastModel, ICoverageModel, IDescModel):
    '''
        保存的栅格数据的info model
        TODO:[*] 20-04-15 现在是否有必要将 store 与 layer 分开存成两个表？
                          此处还欠缺一个 style 的绑定，应该放在 layer中
                          将之前的CoverageModel -> CoverageStoreModel
                          db -> geo_coverage_store
                    +     db -> geo_coverage_layer
                    +     db -> geo_coverageinfo (xx_store + xx_layer)
                         之前在 gsconfig 中 分为 :
                         layer
                         store
                         style
                         是否有必要按照此种方式进行划分
    '''

    class Meta:
        db_table = 'geo_coverageinfo'
