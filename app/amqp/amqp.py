# RabbitMQ based application for MediaGrabber
import pika
import logging
from injector import Injector
from mediagrabber.core import MediaGrabber
from mediagrabber.dependencies import configure
from mediagrabber.config import Config
from app.amqp.consumer import Consumer


def grab(service: MediaGrabber, payload: dict) -> dict:
    urls = service.grab(payload["url"])
    return {"urls": urls}


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

    # Create two consumers for memorize and recognize queues
    service: MediaGrabber = injector.get(MediaGrabber)
    Consumer(service, channel, Config.queue_in(), Config.queue_out(), grab)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()
