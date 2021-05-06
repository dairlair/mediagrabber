from mediagrabber.core import FramesRetrieverInterface, RetrievedFrameResponse
from typing import List
import av
from tqdm import tqdm


class AvFramesRetriever(FramesRetrieverInterface):
    """
    Retrieve images with faces from the given video file.
    Uses the `av` library to read the file.
    """

    def retrieve(self, file: str) -> List[RetrievedFrameResponse]:
        frames = []
        with av.open(file) as container:
            # We only want to look at keyframes.
            stream = container.streams.video[0]
            stream.codec_context.skip_frame = "NONKEY"

            for frame in tqdm(container.decode(stream), "Frames retrieving"):
                ts: float = float(frame.pts * stream.time_base)
                frames.append(RetrievedFrameResponse(ts=ts, pts=frame.pts, img=frame.to_image()))

        return frames
