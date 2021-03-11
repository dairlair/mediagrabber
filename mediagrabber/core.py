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
    def detect(
        self,
        frames: List[Image],
        number_of_upsamples: int = 0,
        locate_model: str = "fog",
        num_jitters: int = 1,
        encode_model: str = "small",
    ) -> List[DetectedFaceResponse]:
        raise NotImplementedError


class FacesPublisherInterface(ABC):
    @abstractmethod
    def publish(self, faces: List[DetectedFaceResponse], path: str):
        raise NotImplementedError


def is_url(self, url: str) -> bool:
    return url.startswith(("http://", "https://"))


class MediaGrabber(ABC):
    @inject
    def __init__(
        self,
        downloader: VideoDownloaderInterface,
        retriever: FramesRetrieverInterface,
        resizer: FramesResizerInterface,
        detector: FacesDetectorInterface,
        publisher: FacesPublisherInterface,
    ):
        self.downloader = downloader
        self.retriever = retriever
        self.resizer = resizer
        self.detector = detector
        self.publisher = publisher

    def download(self, url: str) -> dict:
        return self.downloader.download(url).__dict__

    def retrieve(
        self,
        filename: str,
        resize_height: int = None,
        number_of_upsamples: int = 0,
        locate_model: str = "fog",
        num_jitters: int = 1,
        encode_model: str = "small",
    ):
        """
        Retrieves faces from the specified file.

        Args:
            file (str): Path to the file
            resize_height (int, optional): Desired height for images resizing.
            number_of_upsamples (int, optional): How many times to upsample the image looking for faces.
                Higher numbers find smaller faces.
            locate_model (str, optional): Which face detection model to use. "hog" is less accurate but faster on CPUs.
                "cnn" is a more accurate deep-learning model which is GPU/CUDA accelerated (if available).
            num_jitters (int, optional): How many times to re-sample the face when calculating encoding.
                Higher is more accurate, but slower (i.e. 100 is 100x slower).
            encode_model (str, optional): which model to use. "large" (default) or "small" which only returns 5 points
                but is faster.
        """
        frames: List[Image] = self.retriever.retrieve(filename)
        logging.info(f"{len(frames)} frames retrieved from video file")

        if resize_height is not None:
            frames = self.resizer.resize(frames, resize_height)
            logging.info(f"{len(frames)} frames resized to height {resize_height}")

        faces: List[DetectedFaceResponse] = self.detector.detect(
            frames, number_of_upsamples, locate_model, num_jitters, encode_model
        )
        logging.info(f"{len(faces)} faces found")

        self.publisher.publish(faces, path.realpath(path.dirname(filename)))

    def get_file_path(self, url: str) -> DownloadedVideoResponse:
        if self.is_url(url):
            return self.downloader.download(url).path

        if path.exists(url):
            return url

        raise MediaGrabberError(f'File {url} not found (not URL or existing file)')


