import sys
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

   
# logging.info('this is a logging info message')
# logging.debug('this is a logging debug message')
# logging.warning('this is logging a warning message')
# logging.error('this is an logging error message')
# logging.critical('this is a logging critical message')


import mypika
import myavro
import myutils

if(len(sys.argv) > 6):
    _downloadTaskQueueName = sys.argv[1]
    _user = sys.argv[2]
    _passwd = sys.argv[3]
    _host = sys.argv[4]
    _port = sys.argv[5]

_dev = True
if _dev:
    _downloadTaskQueueName = 'files_handle_req'
    _user = 'pata'
    _passwd = '8888'
    _host = 'amqps.brender.cn'
    _port = 5671


def hanlde_download(filepath):
    pass

def handle_file_hash(filepath):
    pass

def hanlde_upload(filepath):
    pass


def handle(msgbody):
    res = None
    msg = myavro.decode_byte_body(msgbody)
    feedbackQueue = msg['queue']
    code = msg['code']
    uuid = msg['uuid']
    fuid = msg['fuid']
    path = msg['path']
    if code == myprotocol.FileHash:
        fileHash = myqiniu.get_file_hash(path)
        res = myavro.encode(code,fileHash)
    elif code == myprotocol.Download:
        pass
    elif code == myprotocol.Upload:
        pass
    else:
        # default
        pass


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
    logging.info('consumer got queue name is ' + queue)

    channel = mypika.create_channel(_user,_passwd,_host,_port)
    channel.queue_declare(queue=queue, durable=True)
    # print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)
    channel.start_consuming()


def prepare():
    # TODO init works not yet
    # run(_downloadTaskQueueName,callback)
    run(_downloadTaskQueueName,callback)


def main():
    # TODO handle args
    logging.info('start with args : ')
    prepare()

if __name__ == "__main__":
    main()