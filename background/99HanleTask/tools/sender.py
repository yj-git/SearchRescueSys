import pika
import sys
import time
from . import conf

# 这个文件是rabbitmq的发送任务文件，发送到各个客户端


def sendtask(msgp):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=conf.RABBIT_HOST))
    channel = connection.channel()
    # 防止没有队列报错，所以先声明一下
    channel.queue_declare(queue=conf.QUEUE_NAME, durable=True)

    # 发布消息
    channel.basic_publish(
        exchange='',
        # 消息队列名称，随便取，但要与客户端一致
        routing_key='task_queue',
        # 消息主体
        body=msgp,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))

    print(" [x] Sent %r" % msgp)

    connection.close()

    # times = sys.argv[1]
    # message = ' '.join(sys.argv[2:]) or "Ground control this is major Tom "
    # message = ' batch['+str(time.time())+']' + message

    # try:
    #     times = int(times)
    # except:
    #     times = 5

    # for i in range(times):
    #     channel.basic_publish(
    #         exchange='',
    #         routing_key='task_queue',
    #         body=message,
    #         properties=pika.BasicProperties(
    #             delivery_mode=2,  # make message persistent
    #         ))
    #     print(" [x] Sent %r" % message)

    # connection.close()
