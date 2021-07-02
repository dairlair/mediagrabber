from mediagrabber.core import MediaDownloaderInterface, MediaGrabberError
from mediagrabber.downloader.factory import MediaDownloaderFactory
import pytest
from typing import List

@pytest.fixture
def ids() -> List[str]:
    return [
        "direct",
        "youtubedl",
        "ytdlp",
    ]

@pytest.fixture
def factory() -> MediaDownloaderFactory:
    return MediaDownloaderFactory('')

def test_valid_downloader_getting(factory, ids):
    for id in ids:
        downloader = factory.get_media_downloader(id)
        assert issubclass(type(downloader), MediaDownloaderInterface)

def test_unknown_downloader_getting(factory):
    with pytest.raises(MediaGrabberError):
        factory.get_media_downloader('unknown')
