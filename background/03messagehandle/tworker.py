import threading
import pika
import time
import threading
from tlogger import insertLog
import random
import datetime


randseed = 10


# 回调函数，真正的处理函数
def callback(ch, method, propeties, body):
    print(" [R] "+method.consumer_tag +
          " Received %r and logstate:start working" % body)

    # 添加日志
    insertLog(body, 0, method.consumer_tag+' is handling start at' +
              datetime.datetime.now().__str__())

    time.sleep(random.randint(0, randseed))
    print(" [D] "+method.consumer_tag+" Done and logstate end")

    # 更新日志
    insertLog(body, 1, method.consumer_tag+' was finished at' +
              datetime.datetime.now().__str__())


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


threadnum = 5
tlist = []
for i in range(threadnum):
    tlist.append(Mythread(callback, 'thread'+str(i)))


for t in tlist:
    t.start()
