from mediagrabber.retriever.factory import FramesRetrieverFactory
from mediagrabber.downloader.factory import MediaDownloaderFactory
from mediagrabber.storage.postgres import PostgreSQLStorage
from mediagrabber.publisher.base64 import Base64FacePublisher
from mediagrabber.detector.unique import UniqueFaceDetector
from mediagrabber.resizer.default import DefaultFramesResizer
from injector import singleton, Binder
from mediagrabber.core import (
    MediaDownloaderFactoryInterface,
    FacesDetectorInterface,
    FramesResizerInterface,
    MediaGrabber,
    FramesRetrieverFactoryInterface,
    FacesPublisherInterface,
    StorageInterface,
)
from mediagrabber.config import Config
from pika import BlockingConnection, URLParameters
from pika.exceptions import AMQPConnectionError
import sys
import logging
from urllib.parse import urlparse, ParseResult


def configure(binder: Binder) -> None:
    binder.bind(MediaDownloaderFactoryInterface, to=downloader, scope=singleton)
    binder.bind(FramesRetrieverFactoryInterface, to=retriever, scope=singleton)
    binder.bind(FramesResizerInterface, to=resizer, scope=singleton)
    binder.bind(MediaGrabber, to=MediaGrabber, scope=singleton)
    binder.bind(BlockingConnection, amqp, scope=singleton)
    binder.bind(FacesDetectorInterface, to=detector, scope=singleton)
    binder.bind(FacesPublisherInterface, to=publisher, scope=singleton)
    binder.bind(StorageInterface, to=storage, scope=singleton)


def downloader() -> MediaDownloaderFactoryInterface:
    return MediaDownloaderFactory(Config.workdir())


def retriever() -> FramesRetrieverFactoryInterface:
    return FramesRetrieverFactory()


def resizer() -> FramesResizerInterface:
    return DefaultFramesResizer()


def detector() -> FacesDetectorInterface:
    return UniqueFaceDetector()


def publisher() -> FacesPublisherInterface:
    return Base64FacePublisher()


def amqp() -> BlockingConnection:
    try:
        dsn: str = Config.amqp_url()
        return BlockingConnection(parameters=URLParameters(dsn))
    except AMQPConnectionError:
        logging.error("Couldn't connect to the AMQP broker at: [%s]" % dsn)
        sys.exit(2)

def storage() -> StorageInterface:
    dsn: str = Config.dsn()
    parts: ParseResult = urlparse(dsn)

    if parts.scheme == "postgresql":
        return PostgreSQLStorage(dsn)

    raise EnvironmentError(
        """
        Wrong storage DSN provided.
        Must be in the following format:
        postgresql://username:password@hostname:port/database
        """
    )