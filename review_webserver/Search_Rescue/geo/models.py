from django.db import models
from django.utils.timezone import now
# 本项目的
from users.models import IIsDelModel, IArea
from common.models import IIdModel, IDescModel


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


class IForecastModel(models.Model):
    # 时间
    create_date = models.DateTimeField(default=now)

    class Meta:
        abstract = True


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
