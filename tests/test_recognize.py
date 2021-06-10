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
        "tests/data/photos/5faces.jpg",
    ]


class TestRecognize:
    """Ensures that for each memorized face at we can find similar faces
    when we have no limit for distance
    """

    def test_recognize(self, mg, urls):
        memorizedFaceIds: List[int] = []
        # We need to memorize some pictures to lately recognize them
        mg: MediaGrabber = mg
        for url in urls:
            result = mg.memorize(url, "direct", tags=['test_1'])
            for piece in result:
                memorizedFaceIds = memorizedFaceIds + piece["faces"]

        assert len(memorizedFaceIds) > len(urls)

        for faceId in memorizedFaceIds:
            result = mg.recognize(faceId, len(memorizedFaceIds) - 1, tags=['test_1'], tolerance=1)
            assert isinstance(result, List), "Recognize function must return the list"
            for piece in result:
                assert "faces" in piece, "Each piece must have an `faces` field"
                assert len(piece["faces"]) > 0
