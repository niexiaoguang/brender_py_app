import pika
import ssl
import time
import queue
import threading
from pika.credentials import ExternalCredentials

# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='amqp.brender.cn'))
# channel = connection.channel()

# channel.queue_declare(queue='hello')

# channel.basic_publish(exchange='', routing_key='hello', body='Hello World from python!')
# print(" [x] Sent 'Hello World!' from py")
# connection.close()


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
    # body = str(body , encoding = "utf-8")
    q.put(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)




def declare_queue_and_wait(queue,callback):
    print('thread consumer got queue name is ' + queue)
    conn_params = make_conn_params()

    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()

    channel.queue_declare(queue=queue, durable=True)
    # print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)
    channel.start_consuming()


queueName = 'bl_' + str(time.time())

t1 = threading.Thread(target=declare_queue_and_wait, args=(queueName,callback))
t1.start()

print('after threading')
publish('task_queue','my recv queue:' + queueName)
