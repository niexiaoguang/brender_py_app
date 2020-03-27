#!/usr/bin/env python
import pika
import time
import ssl
from pika.credentials import ExternalCredentials

context = ssl.create_default_context(cafile="./ssl/cacert.pem")
context.set_ciphers('ALL:@SECLEVEL=0') # 

context.load_cert_chain(certfile="./ssl/brender-client.cert.pem",
                        keyfile="./ssl/brender-client.key.pem",
                        password="dMokP0brnSeGsphGCfsH41Yr2cwDLauB")

credentials = pika.PlainCredentials('guest', 'guest')
ssl_options = pika.SSLOptions(context, 'amqps.brender.cn')
conn_params = pika.ConnectionParameters(
                                        host='amqps.brender.cn',
                                        port=5671,
                                        ssl_options=ssl_options,
                                        credentials=credentials,
                                        heartbeat=30)

connection = pika.BlockingConnection(conn_params)
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()