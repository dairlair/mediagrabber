import pika

credentials = pika.PlainCredentials('mediagrabber', 'mediagrabber')
virtual_host = 'mediagrabber-vhost'
connection_parameters = pika.ConnectionParameters(host='host.docker.internal', credentials=credentials, virtual_host=virtual_host)
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

channel.queue_declare(queue='hello')

while True:
    channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
    # print(" [x] Sent 'Hello World!'")

connection.close()