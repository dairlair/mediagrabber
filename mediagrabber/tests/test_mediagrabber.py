from mediagrabber.core import MediaGrabber
from mediagrabber.downloader.youtubedl import YoutubedlVideoDownloader
from mediagrabber.retriever.decord import DecordFacesRetriever
from mediagrabber.resizer.default import DefaultFramesResizer
from mediagrabber.detector.unique import UniqueFaceDetector
from mediagrabber.publisher.file import FileFacePublisher


def test_constructor():
    # When
    downloader = YoutubedlVideoDownloader('')
    retriever = DecordFacesRetriever()
    resizer = DefaultFramesResizer()
    detector = UniqueFaceDetector()
    publisher = FileFacePublisher()
    mg: MediaGrabber = MediaGrabber(downloader, retriever, resizer, detector, publisher)

    # Then
    assert type(mg) is MediaGrabber
