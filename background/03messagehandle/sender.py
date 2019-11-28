import pika
import sys
import time


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)


times = sys.argv[1]
message = ' '.join(sys.argv[2:]) or "Ground control this is major Tom "
message = ' batch['+str(time.time())+']' + message

try:
    times = int(times)
except:
    times = 5

for i in range(times):
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    print(" [x] Sent %r" % message)


connection.close()
