from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from PIL import Image, ImageDraw
from injector import inject
import os
import numpy as np
import face_recognition
from tqdm import tqdm


@dataclass
class MediaGrabberError(Exception):
    data: dict


class DownloadedVideoResponse(object):
    size: int = None

    def __init__(self, code: int, output: str, path: str, duration: str):
        self.code = code
        self.output = output
        self.path = path
        self.duration = duration
        self.size = os.path.getsize(path)


class VideoDownloaderInterface(ABC):
    @abstractmethod
    def download(self, video_page_url: str) -> DownloadedVideoResponse:
        raise NotImplementedError


# class SomeFaceResponse(object):
#     id: str

#     def __init__(self, id: str, img: np.array, type: str, coords: List[tuple]):
#         """
#         Creates new instance with the retrieved face data.

#         Contains the image, as a numpy array, unique identified, which can be used for exactly-once
#         further processing guarantee, type ('face' or 'frame') and faces locations, in

#         For the type 'face' the coords will be (0, 0, 0, 0).

#         Args:
#             id (str): Unique image identifier, may be just a '<Frame Number>' for the frame
#                       or '<Frame Number>-<Face Number>' for the face retrieved from the certaint
#                       frame. Can be used for exactly-once further processing guarantee

#             img (np.array): An image (as a numpy array)

#             type (str): 'face' or 'frame'

#             coords (List[tuple]): The tuples list with each face locations in format: (top, right, bottom, left).
#         """
#         self.id = str


class FramesRetrieverInterface(ABC):
    @abstractmethod
    def retrieve(self, file: str) -> List:
        raise NotImplementedError


class StorageInterface(ABC):
    @abstractmethod
    def save(self, content: bytes, name: str) -> str:
        raise NotImplementedError


class MediaGrabber(ABC):
    @inject
    def __init__(self, downloader: VideoDownloaderInterface, retriever: FramesRetrieverInterface):
        self.downloader = downloader
        self.retriever = retriever

    def download(self, url: str) -> List[str]:
        """
        :raises: MediaGrabberError
        """
        vdl: DownloadedVideoResponse = self.downloader.download(url)
        return vdl.__dict__

    def retrieve(self, file: str):
        return self.retriever.retrieve(file)

    def detect(self, file: str):
        frames = self.retrieve(file)
        frame_number = 0
        for frame in tqdm(frames):
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(frame, 0, "fog")
            # face_encodings = face_recognition.face_encodings(frame, face_locations)

            if len(face_locations):
                pil_image = Image.fromarray(frame)
                draw = ImageDraw.Draw(pil_image)

                # Loop through each face found in the unknown image
                face_number = 0
                for (top, right, bottom, left) in face_locations:
                    # Draw a box around the face using the Pillow module

                    outline = (0, 0, 255)
                    face = pil_image.crop(box=(left, top, right, bottom))
                    face.save(f'workdir/faces/face-{frame_number}-{face_number}.png')
                    face_number += 1
                    draw.rectangle(((left, top), (right, bottom)), outline=outline)
                    pil_image.save(f'workdir/frame-{frame_number}.png')

            frame_number += 1


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
