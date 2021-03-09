from mediagrabber.core import FramesRetrieverInterface
from typing import List
import av
# TODO Remove progressbar
from tqdm import tqdm


class AvFacesRetriever(FramesRetrieverInterface):
    """
    Retrieve images with faces from the give video file.
    Uses decord library to read the file.

    Args:
        FacesRetrieverInterface ([type]): [description]
    """
    def retrieve(self, file: str) -> List[]:
        frames = []
        with av.open('/home/dairlair/Videos/Constantine.mkv') as container:
            # Signal that we only want to look at keyframes.
            stream = container.streams.video[0]
            stream.codec_context.skip_frame = 'NONKEY'

            for frame in tqdm(container.decode(stream)):
                frames.append(frame)

        return frames
