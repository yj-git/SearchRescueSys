from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.
# TODO:[-] 20-02-12 注意所有的抽象model命名时加上I(参考c#的接口命名规范)
class IIsDelModel(models.Model):
    is_del = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ICaseBaseStore(models.Model):
    '''
        与存储相关的 抽象model
    '''
    # 根目录
    root_path = models.CharField(max_length=100)
    # 创建的case目录
    case_path = models.CharField(max_length=100)
    # case创建时间
    create_date = models.DateTimeField(editable=False, auto_now_add=True)
    # 预报的时间
    forecast_date = models.DateTimeField(default=now, editable=False)

    class Meta:
        abstract = True


class ICaseBaseModel(models.Model):
    '''
        case 的信息参数 抽象model
    '''
    # 保存case的部分提交的参数
    case_name = models.CharField(max_length=50)
    case_desc = models.CharField(max_length=500)
    # case 的code
    case_code = models.CharField(max_length=50, editable=False, unique=True)

    class Meta:
        abstract = True


class IArea(models.Model):
    CHOISE_TYPE = (
        (-1, 'NULL'),
        (0, 'NORTHWEST'),
        (1, 'CHINASEA'),
        (2, 'EASTCHINASEA'),
    )
    area = models.IntegerField(choices=CHOISE_TYPE, default=-1)

    class Meta:
        abstract = True


class ICaseGeoBaseInfo(models.Model):
    '''
        空间信息(经纬度)相关的 base model 抽象model
    '''

    lat = models.FloatField(null=True, verbose_name="经度")
    lon = models.FloatField(null=True, verbose_name="纬度")

    class Meta:
        abstract = True


class ICaseBaseInfo(models.Model):
    '''
        case的 模型参数 抽象model
    '''
    # 欧拉，龙格库塔法，4阶龙格库塔法
    CHOISE_TYPE = (
        (0, 'Euler'),
        (1, 'Runge'),
        (2, '4Runge'),
    )
    radius = models.FloatField(null=True, verbose_name="释放半径")
    nums = models.IntegerField(null=True, verbose_name="释放粒子数")
    simulation_duration = models.FloatField(null=True, verbose_name="模拟时长")
    simulation_step = models.FloatField(null=True, verbose_name="模拟步长")
    console_step = models.FloatField(null=True, verbose_name="输出步长")
    current_nondeterminacy = models.FloatField(null=True, verbose_name="流场不确定性")
    equation = models.IntegerField(null=True, verbose_name="求解方法", choices=CHOISE_TYPE)

    class Meta:
        abstract = True


class CaseOilInfo(ICaseBaseStore, ICaseBaseModel, ICaseGeoBaseInfo, ICaseBaseInfo, IIsDelModel, IArea):
    '''
        case
    '''
    wind_coefficient = models.FloatField(null=True, verbose_name="风偏系数")
    wind_dir = models.FloatField(null=True, verbose_name="风偏角度")

    # 油品，油量，水温

    class Meta:
        db_table = 'user_caseoilinfo'


class CaseRescueInfo(ICaseBaseStore, ICaseBaseModel, ICaseGeoBaseInfo, ICaseBaseInfo, IIsDelModel, IArea):
    # TODO:[-] 20-02-11 有40多种，等待yyq确认
    goods_type = models.IntegerField(null=True, verbose_name="失事物类型")

    class Meta:
        db_table = 'user_caserescueinfo'


class AuthOilRela(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    did = models.ForeignKey(CaseOilInfo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_authoil_rela'


class AuthRescueRela(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    did = models.ForeignKey(CaseRescueInfo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_authrescue_rela'


class IJobBaseInfo(models.Model):
    CHOISE_TYPE = (
        (0, 'oil'),
        (1, 'rescue'),
    )
    id = models.AutoField(primary_key=True)
    # user_caseinfo的id
    cid = models.IntegerField()
    # celery中保存的id
    job_celery_id = models.CharField(max_length=200)
    # case 的code,注意code不允许重复
    case_code = models.CharField(max_length=50, editable=False, unique=True)
    gmt_create = models.DateTimeField(editable=False, auto_now_add=True)
    gmt_modified = models.DateTimeField(auto_now=True)
    # job的种类(根据创建的作业的种类划分的)
    type = models.IntegerField(default=0, choices=CHOISE_TYPE)

    class Meta:
        abstract = True


class JobInfo(IJobBaseInfo, IIsDelModel, IArea):
    '''
        作业model
            提交的没一个case对应的job

    '''

    class Meta:
        db_table = 'user_jobinfo'


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
    state = models.IntegerField(choices=CHOICE_STATUS, default=2)
    # 需要加入一个创建/修改时间
    gmt_create = models.DateTimeField(default=now, editable=False)
    gmt_modified = models.DateTimeField(default=now)

    class Meta:
        db_table = 'user_jobuserrate'
