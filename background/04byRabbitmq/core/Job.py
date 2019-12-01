import os, path
from abc import ABCMeta, abstractmethod
from datetime import datetime
from enum import Enum
from functools import wraps
import wrapt

from msg.request import MsgRequest
from models.middleModel import OilPatternMidModel


# def write_rate(rate):
#     @wrapt.decorator()
#     def wrapper(func):
#         @wraps(func)
#         def decorated( *args, **kwargs):
#             # 获取request 参数
#             request: MsgRequest = args[1]
#             request.set_content_type_params('rate', rate)
#             return func(request, *args, **kwargs)
#
#         return decorated
#
#     return wrapper

# 带参数的装饰器
# 实现方式1
# def change_rate(rate):
#     '''
#         改变当前作业的进度
#     :param rate:
#     :return:
#     '''
#
#     def decorate(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             # 获取request 参数
#             request: MsgRequest = args[1]
#             request.set_content_type_params('rate', rate)
#             # args[1] = request
#             return func(*args, **kwargs)
#
#         return wrapper
#
#     return decorate

# TODO:[*] 19-11-28对于上面带参数的装饰器的改造，使用了wrapt模块
# 实现方式2
def change_rate(rate):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        # 获取request 参数
        request: MsgRequest = args[0]
        request.set_content_type_params('rate', rate)
        # args[1] = request
        return wrapped(*args, **kwargs)

    return wrapper

# TODO:[-] 19-12-01 改为使用@wrapt.decorator的方式实现，简化部分操作，以下部分注释掉
# def store_job_rate():
#     '''
#        存储当前作业以及当前作业的进度
#     '''
#
#     def decorate(func):
#         @wraps(func)
#         def wrapper(self, *args, **kwargs):
#             # 获取当前作业的信息
#             # 将作业信息以及当前的rate更新至数据库
#             return func(self, *args, **kwargs)
#
#         return wrapper
#
#     return decorate

# TODO:[*] 19-12-01 改为使用@wrapt.decorator的方式实现，简化部分操作
def store_job_rate():
    '''
       存储当前作业以及当前作业的进度
    '''
    @wrapt.decorator
    def wrapper(wrapped,instance,args,kwargs):
        # 获取当前作业的信息
        # 从instance中 获取 job 中的基本信息，以及当前的rate，写入/更新数据库中的记录
        # 将作业信息以及当前的rate更新至数据库
        return wrapped(*args, **kwargs)
    return wrapper


# def write_rate(rate):
#     @wrapt.decorator()
#     def wrapper(wrapped, instance, args, kwargs):
#         # request: MsgRequest = args[0]
#         args[0].set_content_type_params('rate', rate)
#         # args = (request,) + args
#         return wrapped(*args, **kwargs)
#
#     return wrapper


class JobState(Enum):
    '''
        作业的状态：
            主要为 running，computed，waitting 三种
    '''
    RUNNING = 0
    COMPUTED = 1
    WAITTING = 2


class JobBase:
    '''
        基础的作业父类，所有的作业均要继承此类
    '''

    def __init__(self, jobid: str, userid: str, created: datetime, state: JobState = JobState.WAITTING):
        # 当前的作业的状态
        # 默认为等待
        self.state = state
        # 数据库中的作业的id
        self.jobid = jobid
        # 提交作业的用户的id
        self.userid = userid
        # 创建作业的时间
        self.created = created
        #
        pass

    def commit(self):
        '''
            执行完当前作业需要更新数据库中状态
        :return:
        '''
        pass


class JobRun(JobBase):
    '''

    '''

    def __init__(self, jobid: str, userid: str, createdstamp: int, casename: str, dir: str):
        # self.userid = userid
        # self.created = createdstamp
        self.casename = casename
        self.dir = dir
        super().__init__(jobid, userid, createdstamp)

    @property
    def filename(self):
        '''
            根据 userid,时间戳,case名称组合成一个filename
        :return:
        '''
        parts = [self.userid, str(self.created.timestamp()), self.casename]
        filename = '_'.join(parts)
        return filename

    @property
    def fullpath(self):
        '''
            nc文件的的全路径
        :return:
        '''
        fullpath = os.path.join(self.dir, self.filename)
        return fullpath

    def load(self, msg):
        pass

    @abstractmethod
    def doJob(self, **kwargs):
        '''
            执行脚本文件
            需要由继承的类实现的方法
        :return:
        '''


class JobOil(JobRun):
    '''
        一个溢油case
    '''

    def do_job(self, **kwargs):
        '''
            搜救的case主要流程:
                1- 根据传入的参数，执行脚本文件
                2- 将传入的参数写入数据库
                3- 过一段时间去指定路径下获取指定名称的nc文件
                4- 将nc文件写入数据库

        :return:
        '''
        request = MsgRequest()
        self.do_requsest(request)

    def get_request(self, request: MsgRequest):
        '''
            获取传过来的 request
        :param request:
        :return:
        '''
        pass

    @change_rate(rate=10)
    @store_job_rate()
    def do_requsest(self, request: MsgRequest):
        '''
            根据传入的参数执行脚本文件
        :param request:
        :return:
        '''
        oil_pattern: OilPatternMidModel = request.get_content_type_params('oil_pattern')
        # TODO:[*] 19-11-28 下面只是模拟调用脚本的步骤
        print(oil_pattern)
        # 执行之后，向request中写入进度
        # 此处放在装饰器中，不在此处
        # request.set_content_type_params('rate', 0.2)
