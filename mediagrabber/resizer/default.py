from mediagrabber.core import FramesResizerInterface
from typing import List
from tqdm import tqdm
from PIL.Image import Image, ANTIALIAS


class DefaultFramesResizer(FramesResizerInterface):
    def resize(self, frames: List[Image], height: int = 360) -> List[Image]:
        resized_frames: List[Image] = []
        for frame in tqdm(frames):
            orig_width, oring_height = frame.size
            ratio = height / float(oring_height)
            width = int(float(orig_width) * float(ratio))
            resized_frames.append(frame.resize((width, height), ANTIALIAS))

        return resized_frames
