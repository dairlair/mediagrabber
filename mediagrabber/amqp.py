# RabbitMQ based application for MediaGrabber
import pika
from injector import Injector
from mediagrabber.core import MediaGrabber
from dependencies import configure
from mediagrabber.config import Config
from mediagrabber.consumer import Consumer


def grab(service: MediaGrabber, payload: dict) -> dict:
    print("Message received")
    print(payload)
    urls = service.grab(payload.url)
    payload['urls'] = urls
    return payload


if __name__ == "__main__":
    # Dependency Injection setup
    injector = Injector([configure])

    # Just get a pika channel
    connection: pika.BlockingConnection = injector.get(pika.BlockingConnection)
    channel = connection.channel()

    # Create two consumers for memorize and recognize queues
    service: MediaGrabber = injector.get(MediaGrabber)
    Consumer(service, channel, Config.queue_in(), Config.queue_out(), grab)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()
