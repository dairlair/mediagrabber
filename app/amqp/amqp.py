# RabbitMQ based application for MediaGrabber
import pika
import logging
from typing import List
from injector import Injector
from mediagrabber.core import MediaGrabber
from mediagrabber.dependencies import configure
from mediagrabber.config import Config
from app.amqp.consumer import Consumer, MessageProcessorInterface


class MediaGrabberRetriveProcessor(MessageProcessorInterface):
    def __init__(self, service: MediaGrabber) -> None:
        self.service = service

    def process(self, payload: dict) -> List[dict]:
        return self.service.retrieve(**payload)


if __name__ == "__main__":
    # Set desired logging level
    logging.basicConfig(level=Config.log_level())

    # Dependency Injection setup
    injector = Injector([configure])

    # Just get a pika channel
    connection: pika.BlockingConnection = injector.get(pika.BlockingConnection)
    channel = connection.channel()
    # We process a heavy tasks, don't need to prefetch more than one message
    channel.basic_qos(prefetch_count=1)

    # Create consumer
    processor = MediaGrabberRetriveProcessor(injector.get(MediaGrabber))
    Consumer(channel, Config.queue_in(), Config.queue_out(), processor)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()
