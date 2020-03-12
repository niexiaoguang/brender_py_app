import pika
import os
import sys
devHost='10.0.2.2'
args = sys.argv[1:]

scriptpath = "./"

# Add the directory containing your module to the Python path (wants absolute paths)
sys.path.append(os.path.abspath(scriptpath))

# from receive import recv
print(args)
def start():
    print("i'm index file haha")

name = args[0]

def send(name):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=devHost))
    channel = connection.channel()

    channel.queue_declare(queue='hello')
    channel.queue_declare(queue='hello1')

    channel.basic_publish(exchange='', routing_key='hello', body='Hello from ' + name)

    channel.basic_publish(exchange='', routing_key='hello1', body='Hello1 from ' + name)
    print(" [x] Sent 'Hello World!'")
    connection.close()

def recv():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=devHost))
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


send(name)

recv()
