from injector import singleton, Binder
from mediagrabber.core import MediaGrabber, StorageInterface
from mediagrabber.config import Config
from pika import BlockingConnection, URLParameters
from pika.exceptions import AMQPConnectionError
from mediagrabber.core import VideoDownloaderInterface
from mediagrabber.s3 import S3Storage
from mediagrabber.downloader.youtubedl import YoutubedlVideoDownloader
import sys
import logging
from urllib.parse import urlparse, ParseResult


def configure(binder: Binder) -> None:
    binder.bind(VideoDownloaderInterface, to=downloader, scope=singleton)
    # binder.bind(FramerInterface, to=framer, scope=singleton)
    binder.bind(StorageInterface, to=storage, scope=singleton)
    binder.bind(MediaGrabber, to=MediaGrabber, scope=singleton)
    binder.bind(BlockingConnection, amqp, scope=singleton)


# def framer() -> FramerInterface:
#     return OpencvVideoFramesRetriever(Config.workdir(), downloader())


def downloader() -> VideoDownloaderInterface:
    return YoutubedlVideoDownloader(Config.workdir())


def amqp() -> BlockingConnection:
    try:
        dsn: str = Config.amqp_url()
        return BlockingConnection(parameters=URLParameters(dsn))
    except AMQPConnectionError:
        logging.error("Couldn't connect to the AMQP broker at: [%s]" % dsn)
        sys.exit(2)


def storage() -> StorageInterface:
    aws_access_key_id = Config.aws_access_key_id()
    aws_secret_access_key = Config.aws_secret_access_key()
    region = Config.aws_region()
    bucket = Config.aws_bucket()
    return S3Storage(aws_access_key_id, aws_secret_access_key, region, bucket)
