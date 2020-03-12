print("I'm sender")
import os
import sys
import pika
devHost='10.0.2.2'
args = sys.argv[1:]

scriptpath = "./"

# Add the directory containing your module to the Python path (wants absolute paths)
sys.path.append(os.path.abspath(scriptpath))

# from receive import recv
print(args)

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

# recv()
send(name)