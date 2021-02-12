from mediagrabber.meter.meter import MeterInterface
from mediagrabber.meter.providers.null import NullMeter
from mediagrabber.core import MediaGrabber, FramerInterface, StorageInterface
from mediagrabber.framer import OpencvVideoFramesRetriever
from mediagrabber.s3 import S3Storage
from mediagrabber.downloader.youtubedl import YoutubedlVideoDownloader


def test_constructor():
    # When
    meter: MeterInterface = NullMeter()
    framer: FramerInterface = OpencvVideoFramesRetriever("", YoutubedlVideoDownloader(), meter)
    storage: StorageInterface = S3Storage("", "", "", "")
    mg: MediaGrabber = MediaGrabber(framer, storage, meter)

    # Then
    assert type(mg) is MediaGrabber
