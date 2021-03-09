import logging
from decord import VideoReader, cpu
from decord._ffi.base import DECORDError
from mediagrabber.core import FacesRetrieverInterface, RetrievedFaceResponse
from typing import List
# TODO Remove progressbar
from tqdm import tqdm


class DecordFacesRetriever(FacesRetrieverInterface):
    """
    Retrieve images with faces from the give video file.
    Uses decord library to read the file.

    Args:
        FacesRetrieverInterface ([type]): [description]
    """
    def retrieve(self, file: str) -> List[RetrievedFaceResponse]:
        vr = VideoReader(file, ctx=cpu(0))
        length = len(vr)
        fps = int(vr.get_avg_fps())
        print(f'video length: {length}, FPS: {fps}')

        for pos in tqdm(range(0, length, fps * 5)):
            try:
                vr.seek(pos)
                frame = vr.next()
            except DECORDError:
                continue
            # frame = vr[pos].asnumpy()
            # face_locations = face_recognition.face_locations(frame, 1, "fog")
            # if face_locations:
            #     face_encodings = face_recognition.face_encodings(frame, face_locations)

            # if face_locations:
            #     pil_image = Image.fromarray(frame)
            #     draw = ImageDraw.Draw(pil_image)
            #     # for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            #     #     draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
            #     # pil_image.save(workdir + f'/frame-{pos}.png')

        return [RetrievedFaceResponse('1', [], 'face', ())]
