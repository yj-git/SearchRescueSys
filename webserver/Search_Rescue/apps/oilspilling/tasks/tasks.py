from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.decorators import task
import time
import sys

TASK_DIR = r'D:/02proj/SearchRescue/SearchRescueSys/background/04byRabbitmq/'
sys.path.append(TASK_DIR)


# from main import do_job
# import main


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
