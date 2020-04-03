import pika
import ssl
from pika.credentials import ExternalCredentials



def make_conn_params(user,passwd,host,port):

    context = ssl.create_default_context(cafile="./ssl/cacert.pem")
    context.set_ciphers('ALL:@SECLEVEL=0') # 

    context.load_cert_chain(certfile="./ssl/brender-client.cert.pem",
                            keyfile="./ssl/brender-client.key.pem",
                            password="dMokP0brnSeGsphGCfsH41Yr2cwDLauB")


    credentials = pika.PlainCredentials(user, passwd)
    ssl_options = pika.SSLOptions(context, host)
    conn_params = pika.ConnectionParameters(
                                            host=host,
                                            port=port,
                                            ssl_options=ssl_options,
                                            credentials=credentials,
                                            heartbeat=30)
    return conn_params




def publish_msg(queue,msg,user,passwd,host,port):
    conn_params = make_conn_params(user,passwd,host,port)
    with pika.BlockingConnection(conn_params) as conn:
        ch = conn.channel()
        # ch.queue_declare("task_queue")
        ch.queue_declare(queue=queue, durable=True)

        ch.basic_publish("", queue,msg)
        conn.close()

def init():
    pass

def create_channel(user,passwd,host,port):
    conn_params = make_conn_params(user,passwd,host,port)
    # add try except TODO
    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()
    return channel