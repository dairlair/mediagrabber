from mediagrabber.core import FramesRetrieverInterface, RetrievedFrameResponse
from typing import List
from PIL import Image


class PilFramesRetriever(FramesRetrieverInterface):
    """
    Retrieve image from the image file.
    """

    def retrieve(self, file: str) -> List[RetrievedFrameResponse]:
        img = Image.open(file)

        return [RetrievedFrameResponse(0, 0, img)]
