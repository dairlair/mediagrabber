import json
from abc import ABC, abstractmethod
from typing import List
from pika.adapters.blocking_connection import BlockingChannel
import logging


class MessageProcessorInterface(ABC):
    @abstractmethod
    def process(self, payload: dict) -> List[dict]:
        raise NotImplementedError


class Consumer(object):
    """Consumer declares Input Queue and Output Queue, and starts listen the Input Queue.
    Each received message will be passed to the Processor and Processor must return the iterable
    set of messages. Each will be published to the Output Queue and only after that incoming
    message from the Input Queue will be acknowledged.
    """

    def __init__(
        self,
        channel: BlockingChannel,
        queue_in: str,
        queue_out: str,
        processor: MessageProcessorInterface,
    ):
        self.channel = channel
        self.queue_in = queue_out
        self.channel.queue_declare(queue_in, durable=True)
        self.channel.queue_declare(queue_out, durable=True)
        self.processor = processor
        self.channel.basic_consume(queue_in, self.on_message)

    def on_message(self, ch: BlockingChannel, method, properties, body: str):
        # We received message from the incoming queue
        logging.info(f"Incoming message received: {body}")
        payload = json.loads(body)

        # We process this message through processor
        for message in self.processor.process(payload):
            # Merge incoming payload into the each resulting message
            response = {**payload, **message}
            body = json.dumps(response)
            logging.info(f"Outcoming message prepared: {body}")
            self.channel.basic_publish("", self.queue_in, body)

        # We have processed all the messages from the processor, now we ack incoming message
        ch.basic_ack(delivery_tag=method.delivery_tag)
