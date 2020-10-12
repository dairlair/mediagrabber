import json
from pika.adapters.blocking_connection import BlockingChannel
from mediagrabber.core import MediaGrabber
import logging


class Consumer(object):
    def __init__(self, service: MediaGrabber, channel: BlockingChannel, queue_in: str, queue_out: str, callback):
        self.service = service
        self.channel = channel
        self.callback = callback
        self.queue_out = queue_out
        self.channel.queue_declare(queue=queue_in, durable=True)
        self.channel.queue_declare(queue=queue_out, durable=True)
        self.channel.basic_consume(queue=queue_in, on_message_callback=self.on_message)       

    def on_message(self, ch: BlockingChannel, method, properties, body: str):
        logging.info(f'Incoming message received: {body}')
        payload = json.loads(body)
        response = self.callback(self.service, payload)
        if response is None:
            payload = {**payload, 'success': False}
        else:
            payload = {**payload, **response, 'success': True}
        body = json.dumps(payload)
        logging.info(f'Outcoming message prepared: {body}')
        self.channel.basic_publish(exchange="", routing_key=self.queue_out, body=body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
