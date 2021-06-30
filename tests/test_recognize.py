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

@pytest.fixture
def urls_with_tags() -> List[str]:
    return [
        ("tests/data/photos/kira-knightley-1.jpg", ["Kira"]),
        ("tests/data/photos/kira-knightley-2.jpg", ["Kira"]),
        ("tests/data/photos/kira-knightley-3.jpg", ["Kira"]),
        ("tests/data/photos/kira-knightley-4.jpg", ["Kira"]),
        ("tests/data/photos/cercei-lanister-1.jpg", ["Cercei"]),
        ("tests/data/photos/cercei-lanister-2.jpg", ["Cercei"]),
        ("tests/data/photos/cercei-lanister-3.jpg", ["Cercei"]),
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

    def test_recognize_different_tags(self, mg, urls_with_tags):
        mg: MediaGrabber = mg
        lastMemorizedFaceId = None
        for url in urls_with_tags:
            result = mg.memorize(url[0], "direct", tags=url[1])
            for piece in result:
                lastMemorizedFaceId = piece["faces"][-1]
        assert lastMemorizedFaceId is not None

        recognized = mg.recognize(lastMemorizedFaceId, 1, tags=['Kira'], tolerance=1)
