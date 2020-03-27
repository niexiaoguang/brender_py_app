#!/usr/bin/env python
import pika
import time
import ssl
import queue
import threading
from pika.credentials import ExternalCredentials


q = queue.Queue()


def make_conn_params():

    context = ssl.create_default_context(cafile="./ssl/cacert.pem")
    context.set_ciphers('ALL:@SECLEVEL=0') # 

    context.load_cert_chain(certfile="./ssl/brender-client.cert.pem",
                            keyfile="./ssl/brender-client.key.pem",
                            password="dMokP0brnSeGsphGCfsH41Yr2cwDLauB")

    credentials = pika.PlainCredentials('pata', '8888')
    ssl_options = pika.SSLOptions(context, 'amqps.brender.cn')
    conn_params = pika.ConnectionParameters(
                                            host='amqps.brender.cn',
                                            port=5671,
                                            ssl_options=ssl_options,
                                            credentials=credentials,
                                            heartbeat=30)
    return conn_params


def publish(queue,msg):
    conn_params = make_conn_params()
    with pika.BlockingConnection(conn_params) as conn:
        ch = conn.channel()
        # ch.queue_declare("task_queue")
        ch.queue_declare(queue=queue, durable=True)

        ch.basic_publish("", queue,msg)
        conn.close()




def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    body = str(body)
    # q.put(body)
    if('my recv queue' in body):
        qName = body.split(':')[1].split("'")[0]
        print('got queue name put to q ' + qName)
        q.put(qName)
    ch.basic_ack(delivery_tag=method.delivery_tag)

gChann = None

def my_consumer(queue,callback):
    print('thread consumer got queue name is ' + queue)
    conn_params = make_conn_params()

    connection = pika.BlockingConnection(conn_params)
    global gChann
    gChann = connection
    channel = connection.channel()

    channel.queue_declare(queue=queue, durable=True)
    # print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)
    channel.start_consuming()



def loop_send_msg(queue,n):
    for i in range (n):
        publish(queue,str(i))

queueName = 'task_queue'

t1 = threading.Thread(target=my_consumer, args=(queueName,callback))
t1.start()


found = False
while not found:
    time.sleep(1)
    print('inside while')
    print(q.qsize())
    if(q.qsize() > 0):
        queue = q.get()
        print('got from q : ' + queue)
        loop_send_msg(queue,5)
        found = True


print('after loop')

# q.empty()

t1.join()

print('done')