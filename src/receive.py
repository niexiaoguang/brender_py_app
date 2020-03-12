print("I'm receiver")

import pika

devHost='10.0.2.2'

def recv():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=devHost))
    channel = connection.channel()

    channel.queue_declare(queue='hello')
    channel.queue_declare(queue='hello1')


    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    def callback1(ch, method, properties, body):
        print(" [x] Received1 %r" % body)



    channel.basic_consume(
        queue='hello', on_message_callback=callback, auto_ack=True)

    channel.basic_consume(
        queue='hello1', on_message_callback=callback1, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

recv()