from django.db import models
from users.models import CaseOilInfo
from geo.models import CoverageModel
from util.common import DEFAULT_FK, DEFAULT_NULL_KEY


# Create your models here.

class RelaCaseOilCoverageModel(models.Model):
    '''
        TODO:[-] 20-04-27
        用来关联 geo_coverageInfo 与 user_caseoilinfo 表
        有两个外键 分别对应的是 geo_coverageInfo 代表的 流场+风场 的数据(可以为空，不可都为空)
    '''
    id = models.AutoField(primary_key=True)
    '''
        rela.RelaCaseOilCoverage.current_id: (fields.E304) Reverse accessor for 'RelaCaseOilCoverage.current_id' clashes with reverse accessor for 'RelaCaseOilCoverage.wind_id'.
        HINT: Add or change a related_name argument to the definition for 'RelaCaseOilCoverage.current_id' or 'RelaCaseOilCoverage.wind_id'.
rela.RelaCaseOilCoverage.wind_id: (fields.E304) Reverse accessor for 'RelaCaseOilCoverage.wind_id' clashes with reverse accessor for 'RelaCaseOilCoverage.current_id'.
        HINT: Add or change a related_name argument to the definition for 'RelaCaseOilCoverage.wind_id' or 'RelaCaseOilCoverage.current_id'.

    '''
    # wind_id = models.ForeignKey(CoverageModel, on_delete=models.SET_DEFAULT, default=DEFAULT_FK)
    # current_id = models.ForeignKey(CoverageModel, on_delete=models.SET_DEFAULT, default=DEFAULT_FK)
    # case_id = models.ForeignKey(CaseOilInfo, on_delete=models.SET_DEFAULT, default=DEFAULT_FK)

    wind_id = models.IntegerField(default=DEFAULT_FK, null=True)
    current_id = models.IntegerField(default=DEFAULT_FK, null=True)
    case_id = models.IntegerField(default=DEFAULT_FK)

    class Meta:
        db_table = 'rela_case_oil'
