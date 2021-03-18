from mediagrabber.publisher.base64 import Base64FacePublisher
from mediagrabber.publisher.file import FileFacePublisher
from mediagrabber.detector.unique import UniqueFaceDetector
from mediagrabber.resizer.default import DefaultFramesResizer
from mediagrabber.retriever.av import AvFramesRetriever
from injector import singleton, Binder
from mediagrabber.core import (
    FacesDetectorInterface,
    FramesResizerInterface,
    MediaGrabber,
    FramesRetrieverInterface,
    FacesPublisherInterface,
)
from mediagrabber.config import Config
from pika import BlockingConnection, URLParameters
from pika.exceptions import AMQPConnectionError
from mediagrabber.core import VideoDownloaderInterface
from mediagrabber.downloader.youtubedl import YoutubedlVideoDownloader
import sys
import logging


def configure(binder: Binder) -> None:
    binder.bind(VideoDownloaderInterface, to=downloader, scope=singleton)
    binder.bind(FramesRetrieverInterface, to=retriever, scope=singleton)
    binder.bind(FramesResizerInterface, to=resizer, scope=singleton)
    binder.bind(MediaGrabber, to=MediaGrabber, scope=singleton)
    binder.bind(BlockingConnection, amqp, scope=singleton)
    binder.bind(FacesDetectorInterface, to=detector, scope=singleton)
    binder.bind(FacesPublisherInterface, to=publisher, scope=singleton)


def downloader() -> VideoDownloaderInterface:
    return YoutubedlVideoDownloader(Config.workdir())


def retriever() -> FramesRetrieverInterface:
    return AvFramesRetriever()


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
