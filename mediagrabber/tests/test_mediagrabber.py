from mediagrabber.core import MediaGrabber, StorageInterface
from mediagrabber.retriever.decord import DecordFacesRetriever
from mediagrabber.s3 import S3Storage
from mediagrabber.downloader.youtubedl import YoutubedlVideoDownloader


def test_constructor():
    # When
    downloader = YoutubedlVideoDownloader('')
    retriever = DecordFacesRetriever()
    mg: MediaGrabber = MediaGrabber(downloader, retriever)

    # Then
    assert type(mg) is MediaGrabber
