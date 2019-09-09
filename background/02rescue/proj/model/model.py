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
    code=StringField()
    status = IntField()
    time = DateTimeField()
    point = PointField()
    current=EmbeddedDocumentField(CurrentModel)
    wind=EmbeddedDocumentField(WindModel)
