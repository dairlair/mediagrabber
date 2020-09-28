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
    binder.bind(FramerInterface, to=OpencvVideoFramesRetriever("workdir"), scope=singleton)
    binder.bind(StorageInterface, to=create_storage, scope=singleton)
    binder.bind(MediaGrabber, to=MediaGrabber, scope=singleton)
    binder.bind(BlockingConnection, create_blocking_connection, scope=singleton)


def create_blocking_connection() -> BlockingConnection:
    try:
        dsn: str = Config.amqp_url()
        return BlockingConnection(parameters=URLParameters(dsn))    
    except AMQPConnectionError:
        logging.error("Couldn't connect to the AMQP broker. Please, check the AMQP is available with the specified URL: [%s]" % dsn)
        sys.exit(2)


def create_storage() -> StorageInterface:
    aws_access_key_id = 'AKIAIKOOWOEBPSHB5JZQ'
    aws_secret_access_key = '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'
    region = 'us-east-1'
    bucket = 'mediagrabber-dev'
    return S3Storage(aws_access_key_id, aws_secret_access_key, region, bucket)
