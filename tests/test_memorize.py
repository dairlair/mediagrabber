import pytest
from typing import List
from mediagrabber.core import MediaGrabber
from injector import Injector
from mediagrabber.dependencies import configure


@pytest.fixture
def mg() -> MediaGrabber:
    injector = Injector([configure])
    service: MediaGrabber = injector.get(MediaGrabber)
    yield service


@pytest.fixture
def photos_urls() -> List[str]:
    return [
        "https://images.unsplash.com/photo-1517486808906-6ca8b3f04846?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=687&q=100",
    ]


@pytest.fixture
def photos_files() -> List[str]:
    return [
        "tests/data/photos/5faces.jpg",
    ]


@pytest.fixture
def video_urls() -> List[str]:
    return [
        "https://abcnews.go.com/Technology/video/california-judge-orders-uber-lyft-reclassify-drivers-employees-72302309",
    ]


class TestMemorizingFromPhotos:
    def test_memorizing_from_photos_urls(self, mg, photos_urls):
        self.memorizing(mg, photos_urls, "direct")

    def test_memorizing_from_photos_files(self, mg, photos_files):
        self.memorizing(mg, photos_files, "direct")

    def test_memorizing_from_video_urls(self, mg, video_urls):
        self.memorizing(mg, video_urls, "ytdlp")

    def memorizing(self, mg, addresses, downloader="ytdlp"):
        mg: MediaGrabber = mg
        for file in addresses:
            result = mg.memorize(file, downloader)
            assert isinstance(result, List), "The `memorize` response must be a list"
            for piece in result:
                assert "faces" in piece, "Each piece of response must contains faces attributes"
