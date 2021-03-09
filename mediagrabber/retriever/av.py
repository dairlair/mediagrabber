from mediagrabber.core import FramesRetrieverInterface
from typing import List
import av
# TODO Remove progressbar
from tqdm import tqdm
import PIL
import numpy as np


class AvFacesRetriever(FramesRetrieverInterface):
    """
    Retrieve images with faces from the give video file.
    Uses decord library to read the file.

    Args:
        FacesRetrieverInterface ([type]): [description]
    """
    def retrieve(self, file: str) -> List:
        frames = []
        with av.open(file) as container:
            # Signal that we only want to look at keyframes.
            stream = container.streams.video[0]
            stream.codec_context.skip_frame = 'NONKEY'

            for frame in tqdm(container.decode(stream)):

                img_pil = frame.to_image()
                width, height = img_pil.size  # width, height for this read PIL image
                resize_height = 160
                ratio = resize_height / float(height)
                resize_width = int(float(width) * float(ratio))
                img_pil_down = img_pil.resize((resize_width, resize_height), PIL.Image.ANTIALIAS)

                frames.append(np.array(img_pil_down))

        return frames
