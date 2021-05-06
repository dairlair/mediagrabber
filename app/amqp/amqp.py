# RabbitMQ based application for MediaGrabber
import pika
import logging
from typing import List
from injector import Injector
from mediagrabber.core import MediaGrabber
from mediagrabber.dependencies import configure
from mediagrabber.config import Config
from app.amqp.consumer import Consumer, MessageProcessorInterface


class MediaGrabberMemorizeProcessor(MessageProcessorInterface):
    def __init__(self, service: MediaGrabber) -> None:
        self.service = service

    def process(self, payload: dict) -> List[dict]:
        # Payload may contains properties, not intended to be passed to the retrieve function, lets filter them.
        args = {k: v for k, v in payload.items() if k in self.service.memorize.__code__.co_varnames}

        return self.service.memorize(**args)


class MediaGrabberRecognizeProcessor(MessageProcessorInterface):
    def __init__(self, service: MediaGrabber) -> None:
        self.service = service

    def process(self, payload: dict) -> List[dict]:
        # Payload may contains properties, not intended to be passed to the retrieve function, lets filter them.
        args = {k: v for k, v in payload.items() if k in self.service.recognize.__code__.co_varnames}

        return self.service.recognize(**args)


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
    consumersConfigs = [
        {
            "in": Config.queue_memorize(),
            "out": Config.queue_memorized(),
            "processor": MediaGrabberMemorizeProcessor(injector.get(MediaGrabber)),
        },
        {
            "in": Config.queue_recognize(),
            "out": Config.queue_recognized(),
            "processor": MediaGrabberRecognizeProcessor(injector.get(MediaGrabber)),
        }
    ]

    for consumerConfig in consumersConfigs:
        Consumer(channel, consumerConfig["in"], consumerConfig["out"], consumerConfig["processor"])

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()
