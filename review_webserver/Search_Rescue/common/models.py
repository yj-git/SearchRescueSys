from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your views here.
# app为数据字典视图，主要为下拉框提供各类数据支持

CHOIST_TYPE = ((0, 'NULL'),
               # 失事类型
               (1, 'OPTIONWRECK'),
               (2, 'EQUATION'),
               (3, 'NULL'))


class ISelectModel(models.Model):
    '''
        实现了下拉框的抽象model，需要由子model继承
    '''
    # select的名字
    name = models.CharField(max_length=50)
    # 描述
    desc = models.CharField(max_length=50)
    id = models.AutoField(primary_key=True)
    val = models.CharField(max_length=50)
    # 父菜单节点
    parent = models.IntegerField(default=0)
    # 下拉框对应的类型
    type_select = models.IntegerField(choices=CHOIST_TYPE, default=0)

    class Meta:
        abstract = True


class SelectModel(ISelectModel):
    '''
        所有的下拉框数据字典均存储在此处
    '''

    class Meta:
        db_table = 'common_select'