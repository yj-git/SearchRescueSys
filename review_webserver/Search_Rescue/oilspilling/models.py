from django.db import models
# TODO:[*] 20-01-08 注意此处改为使用mongoengine.Doucment，好像之前就是 -_-||
from mongoengine import *

# Create your models here.

# 本项目中的
from rescue.models import WindModel,CurrentModel

class MassModel(EmbeddedDocument):
    '''
       质量相关model
    '''
    # 溢油的质量
    oil = FloatField(default=None)
    # 蒸发的质量
    evaporated = FloatField(default=None)
    # 分散的质量
    dispersed = FloatField(default=None)




class OilModel(EmbeddedDocument):
    '''
        油相关的model
    '''
    # 油的密度
    density = FloatField()
    # 油膜的厚度
    film_thickness = FloatField()

class OilSpillingModel(Document):
    '''
        溢油基础model
    '''
    code = StringField()
    status = IntField()
    time = DateTimeField()
    point = PointField()
    current = EmbeddedDocumentField(CurrentModel)
    wind = EmbeddedDocumentField(WindModel)
    # 海温
    wt = FloatField()
    mass = EmbeddedDocumentField(MassModel)
    # 水含量
    water_fraction = FloatField()

    oil = EmbeddedDocumentField(OilModel)



class OilspillingAvgModel(Document):
    '''
        溢油平均值model
    '''
    code = StringField()
    status = IntField()
    time = DateTimeField()
    point = PointField()
    current = EmbeddedDocumentField(CurrentModel)
    wind = EmbeddedDocumentField(WindModel)
    # 海温
    wt = FloatField()
    mass = EmbeddedDocumentField(MassModel)
    # 水含量
    water_fraction = FloatField()

    oil = EmbeddedDocumentField(OilModel)