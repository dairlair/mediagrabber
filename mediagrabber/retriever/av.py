from mediagrabber.core import FramesRetrieverInterface
from typing import List
import av
from tqdm import tqdm
from PIL.Image import Image


class AvFramesRetriever(FramesRetrieverInterface):
    """
    Retrieve images with faces from the give video file.
    Uses decord library to read the file.
    """

    def retrieve(self, file: str) -> List[Image]:
        frames = []
        with av.open(file) as container:
            # We only want to look at keyframes.
            stream = container.streams.video[0]
            stream.codec_context.skip_frame = "NONKEY"

            for frame in tqdm(container.decode(stream)):
                frames.append(frame.to_image())

        return frames
