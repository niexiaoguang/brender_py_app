import requests
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

   
# logging.info('this is a loggging info message')
# logging.debug('this is a loggging debug message')
# logging.warning('this is loggging a warning message')
# logging.error('this is an loggging error message')
# logging.critical('this is a loggging critical message')


import mypika
import myavro
import myutils


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



def handle(msgbody):
    feedbackQueue = None
    res = None
    return res,feedbackQueue


def callback(ch, method, properties, body):
    logging.info(" [x] Received %r" % body)

    savepath = get_save_file_path(body)
    url = get_url(body)
    feedbackQueue = get_feedback_queue(body)
    download_steam(url,savepath)

    res,feedbackQueue = handle(body)
    # switch handle according msg
    
    mypika.publish_msg(feedbackQueue,res)
    # ack and into linster loop
    ch.basic_ack(delivery_tag=method.delivery_tag)





def run(queue,callback):
    loggging.info('consumer got queue name is ' + queue)

    channel = mypika.create_channel(_user,_passwd,_host,_port)
    channel.queue_declare(queue=queue, durable=True)
    # print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)
    channel.start_consuming()


def prepare():
    # TODO init works not yet
    # run(_downloadTaskQueueName,callback)
    run()


def main():
    # TODO handle args
    loggging.info('start with args : ')
    prepare()

if __name__ == "__main__":
    main()