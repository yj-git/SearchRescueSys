from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.

class CaseInfo(models.Model):
    '''
        case
    '''
    # 根目录
    root_path = models.CharField(max_length=100)
    # 创建的case目录
    case_path = models.CharField(max_length=100)
    # case创建时间
    create_date = models.DateTimeField()
    # 保存case的部分提交的参数
    case_name = models.CharField(max_length=50)
    case_desc = models.CharField(max_length=500)
    # case 的code
    case_code = models.CharField(max_length=50, editable=False)
    lat = models.FloatField(null=True, verbose_name="经度")
    lon = models.FloatField(null=True, verbose_name="纬度")
    wind_coefficient = models.FloatField(null=True, verbose_name="风偏系数")
    wind_dir = models.FloatField(null=True, verbose_name="风偏角度")
    simulation_step = models.FloatField(null=True, verbose_name="模拟步长")
    console_step = models.FloatField(null=True, verbose_name="输出步长")
    current_nondeterminacy = models.FloatField(null=True, verbose_name="流场不确定性")
    equation = models.IntegerField(null=True, verbose_name="求解方法")


class AuthUserDir(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    did = models.ForeignKey(CaseInfo, on_delete=models.CASCADE)


class JobInfo(models.Model):
    '''
        作业model
            提交的没一个case对应的job

    '''
    id = models.AutoField(primary_key=True)
    # user_caseinfo的id
    cid = models.IntegerField()
    # celery中保存的id
    job_id = models.CharField(max_length=200)
    # case 的code
    case_code = models.CharField(max_length=50, editable=False)
    gmt_create = models.DateTimeField(default=now, editable=False)
    gmt_modified = models.DateTimeField(default=now)


class JobUserRate(models.Model):
    '''

    '''

    # 状态共有：1-执行，2-等待，3-结束，4-失败 四种
    CHOICE_STATUS = (
        (1, 'RUNNING'),
        (2, 'WAITTING'),
        (3, 'COMPLETED'),
        (4, 'ERROR'),
        (5, 'UNUSED'),
    )
    id = models.AutoField(primary_key=True)
    jid = models.ForeignKey(JobInfo, on_delete=models.CASCADE)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    # 进度
    rate = models.IntegerField()
    # 状态
    status = models.IntegerField(choices=CHOICE_STATUS, default=2)
    # 需要加入一个创建/修改时间
    gmt_create = models.DateTimeField(default=now, editable=False)
    gmt_modified = models.DateTimeField(default=now)
