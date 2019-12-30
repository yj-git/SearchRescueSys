import threading
import pika
import time
import threading
import random
import datetime
import os
import json

randseed = 10


# 回调函数，真正的处理函数
def callback(ch, method, propeties, body):
    print(" [R] "+method.consumer_tag +
          " Received %r and logstate:start working" % body)

    # 添加日志

    #time.sleep(random.randint(0, randseed))
    handle_task(body)
    print(" [D] "+method.consumer_tag+" Done and logstate end")

    # 更新日志


# 处理事件的方法,目前接收json参数


def handle_task(msgp):
    jsonstr = msgp.decode()
    jobj = json.loads(jsonstr)
    timestr = jobj['Time']
    dirname = timestr.replace(
        '-', '').replace('T', '').replace('Z', '').replace(':', '').split('.')[0][:-2]
    # 生成文件夹
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    print('handle this '+jsonstr)

# 这里面写处理过程，调用什么方法生成文件


def demo():
    pass


class Mythread(threading.Thread):
    def __init__(self, callback, name):
        super(Mythread, self).__init__()
        self.callback = callback
        self.name = name

    # 处理函数
    def work(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='task_queue', durable=True)
        channel.basic_consume(queue='task_queue', auto_ack=True,
                              on_message_callback=self.callback, consumer_tag=self.name)
        print("[*] thread ["+self.name+"] Waiting for message. To exit press CTRL+C")
        channel.start_consuming()

    def run(self):
        self.work()


# 客户端开启的线程数
threadnum = 5
# 客户端线程数列表
tlist = []
for i in range(threadnum):
    tlist.append(Mythread(callback, 'thread'+str(i)))

for t in tlist:
    t.start()
