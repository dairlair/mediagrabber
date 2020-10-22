from mediagrabber.core import MediaGrabber, FramerInterface, StorageInterface
from mediagrabber.framer import OpencvVideoFramesRetriever
from mediagrabber.s3 import S3Storage


def test_constructor():
    # When
    framer: FramerInterface = OpencvVideoFramesRetriever("")
    storage: StorageInterface = S3Storage("", "", "", "")
    mg: MediaGrabber = MediaGrabber(framer, storage)

    # Then
    assert type(mg) is MediaGrabber
