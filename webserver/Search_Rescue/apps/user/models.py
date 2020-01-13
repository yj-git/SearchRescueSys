from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class CaseInfo(models.Model):
    # 根目录
    root_path = models.CharField(max_length=100)
    # 创建的case目录
    case_path = models.CharField(max_length=100)
    # case创建时间
    create_date = models.DateTimeField()
    # 保存case的部分提交的参数
    case_name = models.CharField(max_length=50)
    case_desc = models.CharField(max_length=500)
    lat = models.FloatField(null=True, verbose_name="经度")
    lon = models.FloatField(null=True, verbose_name="纬度")
    wind_coefficient=models.FloatField(null=True,verbose_name="风偏系数")
    wind_dir=models.FloatField(null=True,verbose_name="风偏角度")
    simulation_step=models.FloatField(null=True,verbose_name="模拟步长")
    console_step=models.FloatField(null=True,verbose_name="输出步长")
    current_nondeterminacy=models.FloatField(null=True,verbose_name="流场不确定性")
    equation=models.IntegerField(null=True,verbose_name="求解方法")


class AuthUserDir(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    did = models.ForeignKey(CaseInfo, on_delete=models.CASCADE)
