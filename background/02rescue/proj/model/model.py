from mongoengine import *


class CurrentModel(EmbeddedDocument):
    '''
        海流
    '''
    x = FloatField()
    y = FloatField()


class WindModel(EmbeddedDocument):
    '''
        风
    '''
    x = FloatField()
    y = FloatField()


class MassModel(EmbeddedDocument):
    '''
       质量相关model
    '''
    # 溢油的质量
    oil = FloatField()
    # 蒸发的质量
    evaporated = FloatField()
    # 分散的质量
    dispersed = FloatField()


class OilModel(EmbeddedDocument):
    '''
        油相关的model
    '''
    # 油的密度
    density = FloatField()
    # 油膜的厚度
    film_thickness = FloatField()


class SearchRescueModel(Document):
    '''
        搜救数据
    '''
    code = StringField()
    num = StringField()
    status = IntField()
    time = DateTimeField()
    point = PointField()
    current = EmbeddedDocumentField(CurrentModel)
    wind = EmbeddedDocumentField(WindModel)


class SearchRescueAvgModel(Document):
    '''
        搜救数据
            对数据进行平均计算
    '''
    code = StringField()
    num = StringField()
    status = IntField()
    time = DateTimeField()
    point = PointField()
    current = EmbeddedDocumentField(CurrentModel)
    wind = EmbeddedDocumentField(WindModel)


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
