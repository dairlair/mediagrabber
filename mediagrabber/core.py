from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from injector import inject
import os
import numpy as np


@dataclass
class MediaGrabberError(Exception):
    data: dict


class VideoDownloaderResponse(object):
    size: int = None

    def __init__(self, code: int, output: str, path: str, duration: str):
        self.code = code
        self.output = output
        self.path = path
        self.duration = duration
        self.size = os.path.getsize(path)


class VideoDownloaderInterface(ABC):
    @abstractmethod
    def download(self, video_page_url: str) -> VideoDownloaderResponse:
        raise NotImplementedError


class FacesRetrieverResponse(object):
    id: str

    def __init__(self, id: str, img: np.array, type: str, coords: List[tuple]):
        """
        Creates new instance with the retrieved face data.

        Contains the image, as a numpy array, unique identified, which can be used for exactly-once
        further processing guarantee, type ('face' or 'frame') and faces locations, in

        For the type 'face' the coords will be (0, 0, 0, 0).

        Args:
            id (str): Unique image identifier, may be just a '<Frame Number>' for the frame
                      or '<Frame Number>-<Face Number>' for the face retrieved from the certaint
                      frame. Can be used for exactly-once further processing guarantee

            img (np.array): An image (as a numpy array)

            type (str): 'face' or 'frame'

            coords (List[tuple]): The tuples list with each face locations in format: (top, right, bottom, left).
        """
        self.id = str


class FacesRetrieverInterface(ABC):
    @abstractmethod
    def retrieve(self, file: str) -> List[FacesRetrieverResponse]:
        raise NotImplementedError


class StorageInterface(ABC):
    @abstractmethod
    def save(self, content: bytes, name: str) -> str:
        raise NotImplementedError


class FramerInterface(ABC):
    """
    :raises: MediaGrabberError when url can not be downloaded
    """

    @abstractmethod
    def get_frames(self, video_page_url: str) -> List[bytes]:
        raise NotImplementedError


class MediaGrabber(ABC):
    @inject
    def __init__(self, downloader: VideoDownloaderInterface):
        self.downloader = downloader

    def grab(self, url: str) -> List[str]:
        """
        :raises: MediaGrabberError
        """
        vdl: VideoDownloaderResponse = self.downloader.download(url)
        return vdl.__dict__
