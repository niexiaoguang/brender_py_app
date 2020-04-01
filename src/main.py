import time
import pika
import ssl
from qiniu import etag
import pathlib
from pathlib import Path
from pika.credentials import ExternalCredentials
import requests
import logging
import avro
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
                    
# logging.info('this is a loggging info message')
# logging.debug('this is a loggging debug message')
# logging.warning('this is loggging a warning message')
# logging.error('this is an loggging error message')
# logging.critical('this is a loggging critical message')

_downloadTaskQueueName = sys.argv[1]
_user = sys.argv[2]
_passwd = sys.argv[3]
_host = sys.argv[4]
_port = sys.argv[5]

_dev = True
if _dev:
    _downloadTaskQueueName = 'download_req'
    _user = 'pata'
    _passwd = '8888'
    _host = 'amqps.brender.cn'
    _port = 5671

def get_file_hash(filepath):
    if Path(filepath).if_file():
        return etag(filepath)
    else:
        return None

def download_steam(url,savepath,chunk=2048):
    r = requests.get(url, stream=True)
    with open(savepath, "wb") as f:
        for chunk in r.iter_content(chunk_size=chunk):
            if chunk:
                f.write(chunk)
                # time.sleep(0.1) # speed limit TODO



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


def publish_msg(queue,msg):
    conn_params = make_conn_params(_user,_passwd,_host,_port)
    with pika.BlockingConnection(conn_params) as conn:
        ch = conn.channel()
        # ch.queue_declare("task_queue")
        ch.queue_declare(queue=queue, durable=True)

        ch.basic_publish("", queue,msg)
        conn.close()

def get_save_file_path(data):
    pass

def get_url(data):
    pass

def get_feedback_queue(data):
    pass

def callback(ch, method, properties, body):
    logging.info(" [x] Received %r" % body)
    body = str(body)
    savepath = get_save_file_path(body)
    url = get_url(body)
    feedbackQueue = get_feedback_queue(body)
    download_steam(url,savepath)
    publish_msg(feedbackQueue,'done')
    ch.basic_ack(delivery_tag=method.delivery_tag)





def prepare():
    # TODO init works not yet
    run(_downloadTaskQueueName,callback)

def run(queue,callback):
    loggging.info('consumer got queue name is ' + queue)
    conn_params = make_conn_params(_user,_passwd,_host,_port)

    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()

    channel.queue_declare(queue=queue, durable=True)
    # print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)
    channel.start_consuming()


def main():
    # TODO handle args
    loggging.info('start with args : ')
    prepare()

if __name__ == "__main__":
    main()