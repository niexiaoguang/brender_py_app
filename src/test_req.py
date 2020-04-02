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

recvQueueName = 'recv'



testFilePath = './data/download_task.avsc'

msg = {
        myavro.SchemaNameConst.Code:myavro.Code.FileHash,
        myavro.SchemaNameConst.FilePath:testFilePath,
        myavro.SchemaNameConst.ReQueueName:recvQueueName
        }
byte_msg = myavro.encode_byte_body(myavro.Code.FileHash,msg)

mypika.publish_msg(_fileHandlerQueueName,byte_msg)


def callback(ch, method, properties, body):
    logging.info(" [x] Received %r" % body)
    ch.basic_ack(delivery_tag=method.delivery_tag)





def run(queue,callback):
    logging.info('consumer got queue name is ' + queue)

    channel = mypika.create_channel(_user,_passwd,_host,_port)
    channel.queue_declare(queue=queue, durable=True)
    # print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)
    channel.start_consuming()

run(_fileHandlerQueueName,callback)