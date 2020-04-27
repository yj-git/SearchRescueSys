from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from util.common import DEFAULT_FK, DEFAULT_NULL_KEY
from base.models import IIsDelModel
from geo.models import CoverageModel


# Create your models here.


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
    # forecast_date = models.DateTimeField(default=now, editable=False)
    ext = models.CharField(max_length=20)

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
        (0, 'NORTHWEST'),  # 西北太
        (1, 'CHINASEA'),
        (2, 'EASTCHINASEA'),  # 东中国海
        (3, 'BOHAISEA'),  # 东中国海
        (4, 'INDIAN'),  # 印度洋
        (5, 'SOUTHCHINASEA')  # 南海
        # (6,'NORTHWESTPACIFIC')
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
    wind_nondeterminacy = models.FloatField(null=True, verbose_name="风场不确定性", default=0)
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

    def validate(self, attrs: {}):  # 对多个字段校验
        '''
            根据传入的 attrs 字典，验证并返回符合入库要求的参数字典
            目前实际就是判断不可为null的是否不为null
        :param attrs:
        :return:
        '''
        # 此处应判断是否为null
        # 对于字典的判断最好使用 xx.get('xx')的方式 否则不存在会抛出异常

        # 注释掉
        # if (attrs['root_path'] is '') or (attrs['case_path'] is '') or (attrs['create_date'] is '') or (
        #         attrs['forecast_date'] is '') \
        #         or (attrs['case_name'] is '') or (attrs['case_desc'] is '') or (attrs['case_code'] is '') or (
        #         attrs['area'] is '') \
        #         or (attrs['lat'] is '') or (attrs['lon'] is '') or (attrs['radius'] is '') or (attrs['nums'] is '') \
        #         or (attrs['simulation_duration'] is '') or (attrs['simulation_step'] is '') or (
        #         attrs['console_step'] is '') \
        #         or (attrs['current_nondeterminacy'] is '') or (attrs['equation'] is '') or (attrs['is_del'] is '') \
        #         or (attrs['wind_coefficient'] is '') or (attrs['wind_dir'] is ''):
        #     return None

        # 此处准备改成列表推导
        # 判断 attrs中是否有在指定list中的值为Null的对象，若有则返回None
        # TODO:[-] 20-04-25 使用此种方式完成对于是否为空的判断
        # 方式1:
        un_null_list = ['root_path', 'case_path', 'forecast_data', 'case_name', 'lat', 'lon', 'nums',
                        'wind_coefficient']
        if any([attrs.get(temp) is None for temp in un_null_list]):
            return None

        # 方式2：
        # for temp in un_null_list:
        #     if attrs.get(temp) is None:
        #         return None

        # 方式3:
        # if (attrs.get('root_path') or attrs.get('case_path') or attrs.get('create_date') or
        #         attrs.get('forecast_date')
        #         or attrs.get('case_name') or attrs.get('case_desc') or attrs.get('case_code') or
        #         attrs.get('area')
        #         or attrs.get('lat') or attrs.get(
        #             'lon') or attrs.get('radius') or attrs.get('nums')
        #         or attrs.get('simulation_duration') or
        #         attrs.get('simulation_step') or
        #         attrs.get('console_step')
        #         or attrs.get('current_nondeterminacy') or
        #         attrs.get('equation') or attrs.get('is_del')
        #         or attrs.get('wind_coefficient') or
        #         attrs.get('wind_dir')):
        #     return None

        attrs['case_code'] = self.gen_casecode(attrs.get('case_code'))
        attrs['create_date'] = datetime.strptime(attrs.get('create_date', datetime.utcnow()), '%Y-%m-%d %H:%M:%S')
        attrs['forecast_date'] = datetime.strptime(attrs.get('forecast_date'), '%Y-%m-%d %H:%M:%S')
        attrs['lat'] = float(attrs.get('lat'))
        attrs['lon'] = float(attrs.get('lon'))
        attrs['radius'] = float(attrs.get['radius'])
        attrs['nums'] = int(attrs.get['nums'])
        attrs['simulation_duration'] = float(attrs.get['simulation_duration'])
        attrs['simulation_step'] = float(attrs.get['simulation_step'])
        attrs['console_step'] = float(attrs.get['console_step'])
        attrs['current_nondeterminacy'] = float(attrs.get['current_nondeterminacy'])
        attrs['equation'] = int(attrs.get['equation'])
        attrs['wind_coefficient'] = float(attrs.get['wind_coefficient'])
        attrs['wind_dir'] = float(attrs.get['wind_dir'])
        if attrs['is_del'] == '0':
            attrs['is_del'] = False
        elif attrs['is_del'] == '1':
            attrs['is_del'] = True
        else:
            return None
        return attrs

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
        (2, 'coverage')  # TODO:[-] 20-04-03 +
    )
    id = models.AutoField(primary_key=True)
    # user_caseinfo的id
    # cid = models.IntegerField()
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

    def validate(self, attrs: object):
        '''
            根据传入的 attrs 字典，验证并返回符合入库要求的参数字典
        :param attrs:
        :return:
        '''
        if (attrs['job_celery_id'] is '') or (attrs['case_code'] is '') or (attrs['gmt_create'] is '') or (
                attrs['gmt_modified'] is '') \
                or (attrs['area'] is '') or (attrs['state'] is '') or (attrs['is_del'] is ''):
            return None
        attrs['case_code'] = self.gen_casecode(attrs['case_code'])
        attrs['gmt_create'] = datetime.strptime(attrs['gmt_create'], '%Y-%m-%d %H:%M:%S')
        attrs['gmt_modified'] = datetime.strptime(attrs['gmt_modified'], '%Y-%m-%d %H:%M:%S')
        attrs['area'] = int(attrs['area'])
        attrs['state'] = int(attrs['state'])
        if attrs['is_del'] == '0':
            attrs['is_del'] = False
        elif attrs['is_del'] == '1':
            attrs['is_del'] = True
        else:
            return None
        return attrs

    class Meta:
        db_table = 'user_jobinfo'


# 状态共有：1-执行，2-等待，3-结束，4-失败 四种
CHOICE_STATUS = (
    (1, 'RUNNING'),
    (2, 'COMPLETED'),
    (3, 'WAITTING'),
    (4, 'ERROR'),
    (5, 'UNUSED'),
)


class JobUserRate(models.Model):
    '''

    '''
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


class ITask(models.Model):
    '''
        所有任务的抽象父类
    '''
    # 类型命名规范: eg: '间隔_预报产品类型_区域'
    CHOICE_TYPES = (
        # 流场
        (1, 'DAILY_CURRENT_BHS'),
        (2, 'DAILY_CURRENT_ECS'),  # 东中国海
        (3, 'DAILY_CURRENT_IND'),  # 印度洋
        (4, 'DAILY_CURRENT_SCS'),  # 南海
        (5, 'DAILY_CURRENT_NWP'),  # 西北太
        # 风场
        (6, 'DAILY_WIND_WRF')  # 西北太
    )
    id = models.AutoField(primary_key=True)
    # 数值预报产品种类
    # product_type = models.IntegerField(choices=CHOICE_TYPES, default=-1)
    coverage_type = models.IntegerField(default=DEFAULT_NULL_KEY)
    coverage_area = models.IntegerField(default=DEFAULT_NULL_KEY)
    # 状态
    state = models.IntegerField(choices=CHOICE_STATUS, default=5)

    # TODO:[-] + 20-04-15 加入与 geo_coverageinfo 表 的关联(不要使用外键)
    # TODO:[-] - 20-04-16 去掉了外键关系 放在 -> rela_geo_base 关联表 中
    # coverage_id = models.IntegerField(default=DEFAULT_FK)

    class Meta:
        abstract = True


class TaskUserModel(ITask, ICaseBaseStore):
    '''
        TODO:[-] 20-04-07 + 新添加的 和定时任务有关系的表
    '''

    class Meta:
        db_table = 'user_taskinfo'


class RelaCaseOilCoverage(models.Model):
    '''
        TODO:[-] 20-04-27
        用来关联 geo_coverageInfo 与 user_caseoilinfo 表
        有两个外键 分别对应的是 geo_coverageInfo 代表的 流场+风场 的数据(可以为空，不可都为空)
    '''
    id = models.AutoField(primary_key=True)
    wind_id = models.ForeignKey(CoverageModel, on_delete=models.SET_DEFAULT, default=DEFAULT_FK)
    current_id = models.ForeignKey(CoverageModel, on_delete=models.SET_DEFAULT, default=DEFAULT_FK)
    case_id = models.ForeignKey(CaseOilInfo, on_delete=models.SET_DEFAULT, default=DEFAULT_FK)

    class Meta:
        db_table = 'rela_case_oil'
