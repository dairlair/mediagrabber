from mediagrabber.core import FramesResizerInterface, RetrievedFrameResponse
from typing import List
from tqdm import tqdm
from PIL.Image import ANTIALIAS


class DefaultFramesResizer(FramesResizerInterface):
    def resize(self, frames: List[RetrievedFrameResponse], height: int = 360) -> List[RetrievedFrameResponse]:
        for frame in tqdm(frames):
            assert(isinstance(frame, RetrievedFrameResponse))
            orig_width, oring_height = frame.size
            ratio = height / float(oring_height)
            width = int(float(orig_width) * float(ratio))
            frame.img = frame.img.resize((width, height), ANTIALIAS)

        return frames
