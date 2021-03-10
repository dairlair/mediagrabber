from abc import ABC, abstractmethod
from dataclasses import dataclass
import logging
from os import path
from typing import List
from PIL.Image import Image, fromarray
from injector import inject
import os


@dataclass
class MediaGrabberError(Exception):
    data: dict


class DownloadedVideoResponse:
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


class FramesRetrieverInterface(ABC):
    @abstractmethod
    def retrieve(self, file: str) -> List[Image]:
        """
        Reads the video file and retrieves frames in the Pillow library format.

        Args:
            file (str): Path to the file

        Returns:
            List[Image]: List of PIL Images
        """
        raise NotImplementedError


class FramesResizerInterface(ABC):
    @abstractmethod
    def resize(self, frames: List[Image], height: int = 360) -> List[Image]:
        raise NotImplementedError


@dataclass
class DetectedFaceResponse:
    id: str
    img: Image  # PIL.Image.Image object


class FacesDetectorInterface(ABC):
    @abstractmethod
    def detect(self, frames: List[Image]) -> List[DetectedFaceResponse]:
        raise NotImplementedError

class FacesPublisherInterface(ABC):
    @abstractmethod
    def publish(self, faces: List[DetectedFaceResponse], path: str):
        raise NotImplementedError


class StorageInterface(ABC):
    @abstractmethod
    def save(self, content: bytes, name: str) -> str:
        raise NotImplementedError


class MediaGrabber(ABC):
    @inject
    def __init__(
        self,
        downloader: VideoDownloaderInterface,
        retriever: FramesRetrieverInterface,
        resizer: FramesResizerInterface,
        detector: FacesDetectorInterface,
        publisher: FacesPublisherInterface
    ):
        self.downloader = downloader
        self.retriever = retriever
        self.resizer = resizer
        self.detector = detector
        self.publisher = publisher

    def download(self, url: str) -> List[str]:
        """
        :raises: MediaGrabberError
        """
        return self.downloader.download(url)

    def retrieve(self, file: str):
        return self.retriever.retrieve(file)

    def grab(self, url: str, height: int = 360) -> dict:
        dvr: DownloadedVideoResponse = self.download(url)
        logging.info(f'{dvr.size} bytes video downloaded')

        frames: List[Image] = self.retrieve(dvr.path)
        logging.info(f'{len(frames)} frames retrieved from video file')

        frames = self.resizer.resize(frames, height)
        logging.info(f'{len(frames)} frames resized to height {height}')

        faces: List[DetectedFaceResponse] = self.detector.detect(frames)
        logging.info(f'{len(faces)} faces found')

        self.publisher.publish(faces, path.realpath(path.dirname(dvr.path)))
