import json
from typing import Optional
from pika.adapters.blocking_connection import BlockingChannel
from mediagrabber.core import MediaGrabber, MediaGrabberError
import logging


class MessageProcessor(object):
    def __init__(self, service: MediaGrabber, callback):
        self.service = service
        self.callback = callback

    # Returns dict when message is processed (successfully or with errors).
    def process(self, payload: dict) -> Optional[dict]:
        try:
            response = self.callback(self.service, payload)
            return {**payload, **response, "success": True}
        except MediaGrabberError as err:
            logging.error(err)
            return {**payload, "success": False, "error": err.__dict__}


class Consumer(object):
    def __init__(
        self,
        service: MediaGrabber,
        channel: BlockingChannel,
        queue_in: str,
        queue_out: str,
        callback,
    ):
        self.channel = channel
        self.queue_out = queue_out
        self.channel.queue_declare(queue_in, durable=True)
        self.channel.queue_declare(queue_out, durable=True)
        self.channel.basic_consume(queue_in, self.on_message)
        self.processor = MessageProcessor(service, callback)

    def on_message(self, ch: BlockingChannel, method, properties, body: str):
        logging.info(f"Incoming message received: {body}")

        payload = json.loads(body)
        payload = self.processor.process(payload)
        body = json.dumps(payload)

        logging.info(f"Outcoming message prepared: {body}")
        self.channel.basic_publish("", self.queue_out, body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
