import ssl
import logging

from amqpstorm import Connection
from amqpstorm import Message

logging.basicConfig(level=logging.INFO)

context = ssl.create_default_context(cafile="./ssl/cacert.pem")
context.set_ciphers('ALL:@SECLEVEL=0') # 

context.load_cert_chain(certfile="./ssl/brender-client.cert.pem",
                        keyfile="./ssl/brender-client.key.pem",
                        password="dMokP0brnSeGsphGCfsH41Yr2cwDLauB")

context.verify_mode = ssl.CERT_REQUIRED

ssl_options = {
    'context': context,
    'server_hostname': 'amqps.brender.cn'
}

# ssl_options = {
#     'context': ssl.create_default_context(cafile='./ssl/cacert.pem'),
#     'server_hostname': 'amqps.brender.cn'
# }
def publish_message():
    with Connection('amqps.brender.cn', 'guest', 'guest',port=5671,ssl=True, ssl_options=ssl_options) as connection:
        with connection.channel() as channel:
            # Declare the Queue, 'simple_queue'.
            channel.queue.declare('simple_queue')

            # Message Properties.
            properties = {
                'content_type': 'text/plain',
                'headers': {'key': 'value'}
            }

            # Create the message.
            message = Message.create(channel, 'Hello World!', properties)

            # Publish the message to a queue called, 'simple_queue'.
            message.publish('simple_queue')


if __name__ == '__main__':
    publish_message()