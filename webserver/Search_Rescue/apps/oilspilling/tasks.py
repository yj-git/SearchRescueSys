from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.decorators import task
import time
import sys
from enum import Enum
from datetime import datetime
from abc import ABCMeta, abstractmethod

TASK_DIR = r'D:/02proj/SearchRescue/SearchRescueSys/background/04byRabbitmq/'
sys.path.append(TASK_DIR)


# from main import do_job
# import main
class JobState(Enum):
    '''
        作业的状态：
            主要为 running，computed，waitting 三种
    '''
    RUNNING = 0
    COMPUTED = 1
    WAITTING = 2


class MsgBase:
    def __init__(self):
        pass


class OilModelMsg(MsgBase):
    '''
        提供job之间传递的参数
    '''

    def __init__(self, time: datetime, point: {}, wind_cofficient: float, wind_dir: float, simulation_step: float,
                 console_step: float, current_nondet: float, wind_nondet: float, equation: float, other: {} = None):
        self.time = time
        self.point = point
        self.wind_cofficient = wind_cofficient
        self.wind_dir = wind_dir
        self.simulation_step = simulation_step
        self.console_step = console_step
        self.current_nondet = current_nondet
        self.wind_nondet = wind_nondet
        self.equation = equation
        self.other = other


class Msg:
    '''
        每个job中需要传递的消息msg，包含一些必要的信息
        还需要一些job需要的参数，但是是动态的
    '''

    def __init__(self, name: str, job_name: str, user_id: str, created: datetime, state: JobState, msg: MsgBase):
        self.name = name
        self.job_name: str = job_name
        self.user_id: str = user_id
        self.created: datetime = created
        self.state: JobState = state
        # 需要判断msg是否为继承自MsgBase
        self.msg: MsgBase = msg if isinstance(msg, MsgBase) else None


class Event:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class NCJobBase:
    '''
        需要所有的job继承的父类，有抽象方法handle，需要每个job重写
    '''

    def __init__(self, parent=None):
        self.parent = parent

    def handle(self, even: Event):
        handler = 'handle_{}'.format(even)
        # 判断传入的事件，当前对象是否存在指定方法
        if hasattr(self, handler):
            # 取到当前类的指定方法
            method = getattr(self, handler)
            # 执行该方法
            # 对传入的event事件进行处理
            method(even)
        elif self.parent:
            self.parent.handle(even)
        elif hasattr(self, 'handle_default'):
            self.handle_default(even)

    @abstractmethod
    def handle_default(self, msg: Msg):
        pass



# @shared_task
# TODO:[*] celery 3.1 开始可以通过如下的方式获取task的id
@task(bind=True)
def my_task(self, msg):
    print('测试耗时任务')
    print(f'传入的参数为:{msg}')
    print(f'{self}')
    if hasattr(msg, 'username'):
        print(f'self.request.id:{self.request.id}|{msg.username}')
    print(f'开始调用oil job')
    # print(sys.path)
    # main.do_job()
    # time.sleep(5)
    print('耗时任务结束')
    print('--------------')
