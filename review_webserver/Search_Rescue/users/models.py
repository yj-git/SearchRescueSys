from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import arrow
import pathlib
from computed_property import ComputedCharField

from util.common import DEFAULT_FK, DEFAULT_NULL_KEY
from util.enum import TaskStateEnum
from base.models import IIsDelModel, IArea
from util.customer_exception import LackCoverageError, ConvertError, LackNecessaryFactorError
from Search_Rescue.settings import _ROOT_DIR


# Create your models here.

class ICaseFileBaseStore(models.Model):
    file_name = ComputedCharField(compute_from='get_file_name', max_length=200, default=None, null=True)

    absolute_path = models.CharField(max_length=200, default=None, null=True)
    # 存储的全路径
    # full_path = models.CharField(max_length=200, default=None, null=True)

    full_path = ComputedCharField(compute_from='get_full_path', max_length=200, default=None, null=True)

    @property
    def get_file_name(self):
        case_name = getattr(self, 'case_code')
        ext = getattr(self, 'ext')
        file_name = ''.join([case_name, ext])
        return file_name

    # TODO:[-] 20-05-12 注意由于需要传入 uid，暂时没有办法接受外部传入的参数
    @property
    def get_full_path(self):
        absolute_path = getattr(self, 'absolute_path', None)
        file_name = getattr(self, 'file_name', None)
        full_path = None
        if any([absolute_path, file_name]) is None:
            pass
        else:
            full_path = pathlib.Path(absolute_path) / file_name
        return full_path

    class Meta:
        abstract = True


class ICaseBaseStore(models.Model):
    '''
        与存储相关的 抽象model
    '''
    # 根目录
    root_path = models.CharField(max_length=100)
    #
    # 创建的case目录
    case_path = models.CharField(max_length=100)
    # 文件名称
    # file_name = models.CharField(max_length=100, default=None, null=True)
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
    case_desc = models.CharField(max_length=500, null=True)
    # case 的code
    case_code = models.CharField(max_length=50, editable=False, unique=True)

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


class CaseOilInfo(ICaseBaseStore, ICaseBaseModel, ICaseGeoBaseInfo, ICaseBaseInfo, IIsDelModel, IArea,
                  ICaseFileBaseStore):
    '''
        case
    '''
    id = models.AutoField(primary_key=True)
    wind_coefficient = models.FloatField(null=True, verbose_name="风偏系数")
    wind_dir = models.FloatField(null=True, verbose_name="风偏角度")

    # 油品，油量，水温

    # def __gen_casecode(self, code):
    #     '''
    #         根据传入的 code 参数，生成带时间戳的case_code编码
    #     :param code:
    #     :return:
    #     '''
    #     dt_ms = datetime.now().strftime('%Y%m%d%H%M%S%f')
    #     case_code = code + '_' + dt_ms
    #     return case_code

    # def _gen_casecode(self, code):
    #     dt_ms = datetime.now().strftime('%Y%m%d%H%M%S%f')
    #     case_code = code + '_' + dt_ms
    #     return case_code

    # @classmethod
    def gen_casecode(self, code: str, current: datetime):
        '''
            TODO:[-] 20-05-11 此处之前存在一个逻辑bug，不可以通过获取当前的事件生成gen_casecode ，由于再多处调用，会存在生成的code不唯一的问题
        :param code:
        :param current:
        :return:
        '''
        # 此处的 时间的标识改为时间戳
        datetime_arrow = arrow.get(current)

        dt_ms = datetime_arrow.timestamp
        case_code = code + '_' + str(dt_ms)
        return case_code

    # @classmethod
    def _test_gen(cls):
        return 'ceshi'

    # @classmethod
    def validate(self, attrs: {}):  # 对多个字段校验
        '''
            根据传入的 attrs 字典，验证并返回符合入库要求的参数字典
            目前实际就是判断不可为null的是否不为null
        :param attrs:
        :return:
        '''
        # 此处应判断是否为null
        # 对于字典的判断最好使用 xx.get('xx')的方式 否则不存在会抛出异常

        # 此处准备改成列表推导
        # 判断 attrs中是否有在指定list中的值为Null的对象，若有则返回None
        # TODO:[-] 20-04-25 使用此种方式完成对于是否为空的判断
        # 方式1:
        un_null_list = ['forecast_date', 'case_name', 'lat', 'lon', 'nums',
                        'wind_coefficient', 'type']
        # TODO:[*] 20-04-28 住一次出存在一个问题就是若提交的 params中有 current_coverage_id 字段，但是为''，则还是会有问题
        # 此处的逻辑为: 两个id 起码有一个为非空=不能全为空=!全为空
        if all([attrs.get('wind_coverage_id', None) is None, attrs.get('current_coverage_id', None) is None]):
            raise LackCoverageError('lack wind or current coverage id')
        if any([attrs.get(temp) is None for temp in un_null_list]):
            raise LackNecessaryFactorError('lack neccessary facotr from case oil')
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

        # attrs['case_code'] = self.__gen_casecode(attrs.get('case_code'))
        try:

            # 若自动创建的时间是utc时间
            attrs['create_date'] = arrow.get(attrs.get('create_date')).datetime if attrs.get('create_date',
                                                                                             None) not in ['',
                                                                                                           None] else arrow.utcnow().datetime
            #
            attrs['case_code'] = self.gen_casecode(attrs.get('case_code'), attrs['create_date'])
            # test_code = self._test_gen()
            # 预报时间由前台传入为 gmt 时间(非utc时间)
            attrs['forecast_date'] = arrow.get(attrs.get('forecast_date')).datetime
            attrs['lat'] = float(attrs.get('lat'))
            attrs['lon'] = float(attrs.get('lon'))
            attrs['radius'] = float(attrs.get('radius')) if attrs.get('radius') is not None else None
            attrs['nums'] = int(attrs.get('nums')) if attrs.get('nums') is not None else None
            attrs['simulation_duration'] = float(attrs.get('simulation_duration')) if attrs.get(
                'simulation_duration') is not None else None
            attrs['simulation_step'] = float(attrs.get('simulation_step')) if attrs.get(
                'simulation_step') is not None else None
            attrs['console_step'] = float(attrs.get('console_step')) if attrs.get('console_step') is not None else None
            attrs['current_nondeterminacy'] = float(attrs.get('current_nondeterminacy')) if attrs.get(
                'current_nondeterminacy') is not None else None
            attrs['equation'] = int(attrs.get('equation')) if attrs.get('equation') is not None else None
            attrs['wind_coefficient'] = float(attrs.get('wind_coefficient')) if attrs.get(
                'wind_coefficient') is not None else None
            attrs['wind_dir'] = float(attrs.get('wind_dir')) if attrs.get('wind_dir') is not None else None
            if attrs['is_del'] == '0':
                attrs['is_del'] = False
            elif attrs['is_del'] == '1':
                attrs['is_del'] = True
            else:
                attrs['is_del'] = False
            return attrs
        except Exception as e:
            raise ConvertError('convert error')

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
        (2, 'coverage')  # TODO:[*] 20-04-29 + 此处需要与 枚举类映射起来
    )
    id = models.AutoField(primary_key=True)
    # user_caseinfo的id
    # cid = models.IntegerField()
    # celery中保存的id
    job_celery_id = models.CharField(max_length=200, null=True)
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

    def validate(self, attrs: {}):
        '''
            根据传入的 attrs 字典，验证并返回符合入库要求的参数字典
        :param attrs:
        :return:
        '''
        un_null_list = ['case_code']
        if any([attrs.get(temp) is None for temp in un_null_list]):
            return None

        if (attrs['job_celery_id'] is '') or (attrs['case_code'] is '') or (attrs['gmt_create'] is '') or (
                attrs['gmt_modified'] is '') \
                or (attrs['area'] is '') or (attrs['state'] is '') or (attrs['is_del'] is ''):
            return None
        attrs['case_code'] = attrs['case_code']
        attrs['gmt_create'] = arrow.get(attrs.get('gmt_create')).datetime if attrs.get('gmt_create',
                                                                                       None) not in ['',
                                                                                                     None] else arrow.utcnow().datetime
        attrs['gmt_modified'] = arrow.get(attrs.get('gmt_modified')).datetime if attrs.get('gmt_modified',
                                                                                           None) not in ['',
                                                                                                         None] else arrow.utcnow().datetime
        attrs['area'] = int(attrs['area'])
        attrs['start_time'] = arrow.get(attrs.get('start_time')).datetime if attrs.get('start_time',
                                                                                       None) not in ['',
                                                                                                     None] else arrow.utcnow().datetime
        attrs['end_time'] = arrow.get(attrs.get('end_time')).datetime if attrs.get('end_time',
                                                                                   None) not in ['',
                                                                                                 None] else arrow.utcnow().datetime
        attrs['area'] = int(attrs['area'])
        # attrs['state'] = int(attrs['state'])
        # attrs['state'] = attrs.get('state', None)
        attrs['state'] = int(attrs['state']) if attrs['state'] is not None else TaskStateEnum.RUNNING.value
        attrs['is_del'] = False
        # TODO:[-] 20-04-30 注意将 rela_case_coverage 中需要判断的 current_id 与 wind_id 放在 users/models 中格式化
        attrs['current_id'] = int(attrs['current_id'] if attrs['current_id'] is not None else DEFAULT_NULL_KEY)
        attrs['wind_id'] = int(attrs['wind_id'] if attrs['wind_id'] is not None else DEFAULT_NULL_KEY)
        # TODO:[-] 20-05-11 新加入了 type_job
        attrs['type_job'] = int(attrs.get('type_job'))
        # if attrs['is_del'] == '0':
        #     attrs['is_del'] = False
        # elif attrs['is_del'] == '1':
        #     attrs['is_del'] = True
        # else:
        #     return None
        return attrs

    class Meta:
        db_table = 'user_jobinfo'


# 状态共有：1-执行，2-等待，3-结束，4-失败 四种
# TODO:[*] 20-05-07 此处与枚举 enmu.py -> TaskStateEnum 相对应，此处如果处理使 enum -> 元祖
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
