#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/22 4:52 下午
# @Author  : evaseemefly
# @Desc    : celery相关的配置
# @Site    : 
# @File    : settings.py
# @Software: PyCharm

# 使用RabbitMQ作为消息代理
BROKER_URL=f'amqp://admin:admin123@localhost:5672/'
# 把任务结果存在了Redis
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# 任务序列化和反序列化使用JSON方案
CELERY_TASK_SERIALIZER = 'json'
# 读取任务结果使用JSON
CELERY_RESULT_SERIALIZER = 'json'
# 任务过期时间，不建议直接写86400，应该让这样的magic数字表述更明显
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
# 指定接受的内容类型，是个数组，可以写多个
CELERY_ACCEPT_CONTENT = ['json']