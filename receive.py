import pika
import time

credentials = pika.PlainCredentials('mediagrabber', 'mediagrabber')
virtual_host = 'mediagrabber-vhost'
connection_parameters = pika.ConnectionParameters(host='host.docker.internal', credentials=credentials, virtual_host=virtual_host)
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

channel.queue_declare(queue='hello')

count: int = 0
start_time: float = time.time()

def callback(ch, method, properties, body):
    global count
    count += 1
    rps = count / (time.time() - start_time)
    if (count % 10000 == 0):
        print(f"\rRPS: {rps}" % body)


channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()