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
