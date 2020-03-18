import pika
import ssl
from pika.credentials import ExternalCredentials

# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='amqp.brender.cn'))
# channel = connection.channel()

# channel.queue_declare(queue='hello')

# channel.basic_publish(exchange='', routing_key='hello', body='Hello World from python!')
# print(" [x] Sent 'Hello World!' from py")
# connection.close()


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




# context = ssl.create_default_context(cafile="./ssl/cacert.pem")
# context.load_cert_chain("./ssl/brender-client_cert.pem",
#                         "./ssl/brender-client_key.pem",
#                         "dMokP0brnSeGsphGCfsH41Yr2cwDLauB")
# ssl_options = pika.SSLOptions(context, "amqps.brender.cn")
# conn_params = pika.ConnectionParameters(port=5671,
#                                         ssl_options=ssl_options)

with pika.BlockingConnection(conn_params) as conn:
    ch = conn.channel()
    ch.queue_declare("foobar")
    ch.basic_publish("", "foobar", "Hello, world! with ssl ")
    # print(ch.basic_get("foobar"))