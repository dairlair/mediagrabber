from injector import singleton, Binder
from mediagrabber.core import MediaGrabber, FramerInterface, StorageInterface
from mediagrabber.config import Config
from pika import BlockingConnection, URLParameters
from pika.exceptions import AMQPConnectionError
from mediagrabber.framer import OpencvVideoFramesRetriever
from mediagrabber.s3 import S3Storage

import sys
import logging


def configure(binder: Binder) -> None:
    binder.bind(FramerInterface, to=create_framer, scope=singleton)
    binder.bind(StorageInterface, to=create_storage, scope=singleton)
    binder.bind(MediaGrabber, to=MediaGrabber, scope=singleton)
    binder.bind(BlockingConnection, create_amqp_connection, scope=singleton)


def create_framer() -> FramerInterface:
    return OpencvVideoFramesRetriever(Config.workdir())


def create_amqp_connection() -> BlockingConnection:
    try:
        dsn: str = Config.amqp_url()
        return BlockingConnection(parameters=URLParameters(dsn))
    except AMQPConnectionError:
        logging.error("Couldn't connect to the AMQP broker at: [%s]" % dsn)
        sys.exit(2)


def create_storage() -> StorageInterface:
    aws_access_key_id = Config.aws_access_key_id()
    aws_secret_access_key = Config.aws_secret_access_key()
    region = Config.aws_region()
    bucket = Config.aws_bucket()
    return S3Storage(aws_access_key_id, aws_secret_access_key, region, bucket)
