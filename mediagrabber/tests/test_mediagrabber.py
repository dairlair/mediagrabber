from mediagrabber.core import MediaGrabber, FramerInterface, StorageInterface
from mediagrabber.framer import OpencvVideoFramesRetriever
from mediagrabber.s3 import S3Storage
from mediagrabber.downloader.youtubedl import YoutubedlVideoDownloader


def test_constructor():
    # When
    framer: FramerInterface = OpencvVideoFramesRetriever(
        "", YoutubedlVideoDownloader()
    )
    storage: StorageInterface = S3Storage("", "", "", "")
    mg: MediaGrabber = MediaGrabber(framer, storage)

    # Then
    assert type(mg) is MediaGrabber
