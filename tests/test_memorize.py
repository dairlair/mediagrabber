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
def urls() -> List[str]:
    return [
        "https://images.unsplash.com/photo-1517486808906-6ca8b3f04846?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=687&q=100",
    ]


class TestMemorizingFromPhotos:
    def test_faces_memorizing_from_photos(self, mg, urls):
        mg: MediaGrabber = mg
        for url in urls:
            result = mg.memorize(url, "direct")
            assert isinstance(result, List), "The `memorize` response must be a list"
            for piece in result:
                assert "faces" in piece, "Each piece of response must contains faces attributes"
