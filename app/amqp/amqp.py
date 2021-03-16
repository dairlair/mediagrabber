# RabbitMQ based application for MediaGrabber
import pika
import logging
from injector import Injector
from mediagrabber.core import MediaGrabber
from mediagrabber.dependencies import configure
from mediagrabber.config import Config
from app.amqp.consumer import Consumer


def retrieve(service: MediaGrabber, payload: dict) -> dict:
    urls = service.retrieve(payload["url"])
    return {"urls": urls}

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
    service: MediaGrabber = injector.get(MediaGrabber)
    Consumer(service, channel, Config.queue_in(), Config.queue_out(), retrieve)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()
