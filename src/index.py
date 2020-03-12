import pika
import os
import sys
import ssl
from pika.credentials import ExternalCredentials


amqp_host= 'ampqs:amqp.brender.cn'
# amqp_host= '182.92.200.86'
args = sys.argv[1:]

scriptpath = "./"

# Add the directory containing your module to the Python path (wants absolute paths)
sys.path.append(os.path.abspath(scriptpath))

# from receive import recv
print(args)
def start():
    print("i'm index file haha")

name = args[0]

ssl_options = {    
    "ca_certs":"./ssl/cacert.pem",
    "certfile": "./ssl/client/rabbit-client.cert.pem",
    "keyfile": "./ssl/client/rabbit-client.key.pem",
    "cert_reqs": ssl.CERT_REQUIRED,
    "ssl_version":ssl.PROTOCOL_TLSv1_2
}

def connect():
    # credentials = pika.PlainCredentials('test', 'test')
    # parameters = pika.ConnectionParameters(host=amqp_host,
    #                                        port=5671,
    #                                        virtual_host='/',
    #                                        heartbeat_interval = 30,
    #                                        credentials=credentials,
    #                                        ssl = True,
    #                                        ssl_options = ssl_options)
    # connection = pika.BlockingConnection(parameters)
    # print(connection)
    # connection.close()



    # context = ssl.create_default_context(cafile="./ssl/cacert.pem")
    # context.load_cert_chain(certfile="./ssl/client/rabbit-client.cert.pem",keyfile="./ssl/client/rabbit-client.key.pem",password="PLE427VKgNSpqEXN")
    # ssl_options = pika.SSLOptions(context, amqp_host)
    # conn_params = pika.ConnectionParameters(port=5671,ssl_options=ssl_options)

    # with pika.BlockingConnection(conn_params) as conn:
    #     ch = conn.channel()
    #     ch.queue_declare("hello")
    #     ch.basic_publish("", "hello", "Hello, world!")
    #     print(ch.basic_get("hello"))




    context = ssl.create_default_context(cafile="./ssl/cacert.pem")

    # I know it's much better to use another certificate but sometimes there is no choise:
    # I know it's very rude solution. Use it as start point

    context.set_ciphers('ALL:@SECLEVEL=0') # 

    context.load_cert_chain(certfile="./ssl/client/rabbit-client.cert.pem",keyfile="./ssl/client/rabbit-client.key.pem",password="PLE427VKgNSpqEXN")
    # context.set_ciphers('ALL:@SECLEVEL=0')

    ssl_options = pika.SSLOptions(context, amqp_host)
    conn_params = pika.ConnectionParameters(host=amqp_host,
                                            port=5671,
                                            # virtual_host="/",
                                            ssl_options=ssl_options,
                                            credentials=ExternalCredentials())



    with pika.BlockingConnection(conn_params) as conn:
         ch = conn.channel()
         ch.queue_declare("hello")
         ch.basic_publish("", "hello", "Hello, world from python!")
         print(ch.basic_get("hello"))



    # cp = pika.ConnectionParameters(amqp_host, 5671, '/',
    #                                 ssl=True,
    #                                 ssl_options=dict(
    #                                     ssl_version=ssl.PROTOCOL_TLSv1,
    #                                     ca_certs="./ssl/cacert.pem",
    #                                     keyfile="./ssl/client/rabbit-client.key.pem",
    #                                     certfile="./ssl/client/rabbit-client.cert.pem",
    #                                     cert_reqs=ssl.CERT_REQUIRED)
    #                                 )


    # with pika.BlockingConnection(cp) as conn:
    #      ch = conn.channel()
    #      ch.queue_declare("hello")
    #      ch.basic_publish("", "hello", "Hello, world from python!")
    #      print(ch.basic_get("hello"))


connect()


def send(name):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=amqp_host))
    channel = connection.channel()

    channel.queue_declare(queue='hello')
    channel.queue_declare(queue='hello1')

    channel.basic_publish(exchange='', routing_key='hello', body='Hello from ' + name)

    channel.basic_publish(exchange='', routing_key='hello1', body='Hello1 from ' + name)
    print(" [x] Sent 'Hello World!'")
    connection.close()

def recv():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=amqp_host))
    channel = connection.channel()

    channel.queue_declare(queue='hello')
    channel.queue_declare(queue='hello1')


    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    # def callback1(ch, method, properties, body):
    #     print(" [x] Received1 %r" % body)



    channel.basic_consume(
        queue='hello', on_message_callback=callback, auto_ack=True)

    # channel.basic_consume(
        # queue='hello1', on_message_callback=callback1, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


