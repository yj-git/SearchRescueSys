from django.db import models
from django.utils.timezone import now
# 本项目的
from users.models import IIsDelModel, IArea


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


class IForecastModel(models.Model):
    # 时间
    create_date = models.DateTimeField(default=now)


class ICoverageModel(models.Model):
    '''
        所有的栅格文件的父类
    '''
    # 维度数组 只存维度的 名称
    dimessions = models.CharField(default='')
    # 特征变量数组
    variables = models.CharField(default='')

    class Meta:
        abstract = True


class CoverageModel(IArea, IIsDelModel, IStoreModel, IForecastModel, ICoverageModel):
    '''
        保存的栅格数据的info model
    '''
    class Meta:
        db_table = 'geo_coverageinfo'
