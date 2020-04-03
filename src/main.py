import sys
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

   
# logging.info('this is a logging info message')
# logging.debug('this is a logging debug message')
# logging.warning('this is logging a warning message')
# logging.error('this is an logging error message')
# logging.critical('this is a logging critical message')


import mypika
import myavro
import myutils
import myqiniu

if(len(sys.argv) > 6):
    _fileHandlerQueueName = sys.argv[1]
    _user = sys.argv[2]
    _passwd = sys.argv[3]
    _host = sys.argv[4]
    _port = sys.argv[5]

_dev = True
if _dev:
    _fileHandlerQueueName = 'files_handle_req'
    _user = 'pata'
    _passwd = '8888'
    _host = 'amqps.brender.cn'
    _port = 5671


def hanlde_download(filepath):
    pass

def handle_file_hash(msg):
        filePath = msg[myavro.SchemaNameConst.Data]
        fileHash = myqiniu.get_file_hash(filePath)
        data = {
            myavro.SchemaNameConst.Code:myavro.Code.FileHash,
            myavro.SchemaNameConst.Data:fileHash,
            myavro.SchemaNameConst.Status:200,
            myavro.SchemaNameConst.Sender:'brender_files_handler' #mayby use unique name TODO
            }
        res = myavro.encode_byte_body(data)
        return res


def hanlde_upload(filepath):
    pass


def handle(msgbody):
    res = None
    msg = myavro.decode_byte_body(msgbody)

    code = msg[myavro.SchemaNameConst.Code]
    replyQueueName = msg[myavro.SchemaNameConst.Sender]

    if code == myavro.Code.FileHash:
        res = handle_file_hash(msg)
    elif code == myavro.Code.Download:
        pass
    elif code == myavro.Code.Upload:
        pass
    else:
        # default
        pass


    return res,replyQueueName


def callback(ch, method, properties, body):
    logging.info(" [x] Received %r" % body)

    res,replyQueueName = handle(body)
    # switch handle according msg
    
    mypika.publish_msg(replyQueueName,res,_user,_passwd,_host,_port)
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
    # run(_fileHandlerQueueName,callback)
    run(_fileHandlerQueueName,callback)


def main():
    # TODO handle args
    print('start with args : ')
    prepare()

if __name__ == "__main__":
    main()