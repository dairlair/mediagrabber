from mediagrabber.core import MediaGrabber
from mediagrabber.downloader.factory import MediaDownloaderFactory
from mediagrabber.retriever.factory import FramesRetrieverFactory
from mediagrabber.resizer.default import DefaultFramesResizer
from mediagrabber.detector.unique import UniqueFaceDetector
from mediagrabber.publisher.file import FileFacePublisher
from mediagrabber.distancer.annoy import AnnoyDistancer
from mediagrabber.storage.postgres import PostgreSQLStorage


def test_constructor():
    # When
    retriever_factory = FramesRetrieverFactory()
    resizer = DefaultFramesResizer()
    detector = UniqueFaceDetector()
    publisher = FileFacePublisher()
    downloader_factory = MediaDownloaderFactory("")
    storage = PostgreSQLStorage("postgresql://localhost:5432/db")
    distancer = AnnoyDistancer(storage)
    mg: MediaGrabber = MediaGrabber(
        retriever_factory, resizer, detector, publisher, storage, downloader_factory, distancer
    )

    # Then
    assert type(mg) is MediaGrabber
