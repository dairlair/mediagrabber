from abc import ABC, abstractmethod
from dataclasses import dataclass
import logging
from os import path
from typing import List, Optional
from PIL.Image import Image
from injector import inject
import os
import numpy as np


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
        if path is not None:
            self.size = os.path.getsize(path)


class VideoDownloaderInterface(ABC):
    @abstractmethod
    def download(self, video_page_url: str) -> DownloadedVideoResponse:
        raise NotImplementedError


@dataclass
class RetrievedFrameResponse:
    ts: float
    pts: int
    img: Image


class FramesRetrieverInterface(ABC):
    @abstractmethod
    def retrieve(self, file: str) -> List[RetrievedFrameResponse]:
        """
        Reads the video file and retrieves frames in the Pillow library format.

        Args:
            file (str): Path to the file

        Returns:
            List[RetrievedFrameResponse]: List of the retrieved frames
        """
        raise NotImplementedError


class FramesResizerInterface(ABC):
    @abstractmethod
    def resize(self, frames: List[RetrievedFrameResponse], height: int = 360) -> List[RetrievedFrameResponse]:
        raise NotImplementedError


@dataclass
class DetectedFaceResponse:
    """
    id: str The face number on the frame
    """

    id: str
    img: Image
    ts: float
    pts: int
    box: dict
    encoding: np.ndarray


class FacesDetectorInterface(ABC):
    @abstractmethod
    def detect(
        self,
        frames: List[RetrievedFrameResponse],
        number_of_upsamples: int = 0,
        locate_model: str = "fog",
        num_jitters: int = 1,
        encode_model: str = "small",
        tolerance: float = 0.6,
    ) -> List[DetectedFaceResponse]:
        raise NotImplementedError


class FacesPublisherInterface(ABC):
    @abstractmethod
    def publish(self, faces: List[DetectedFaceResponse], path: str) -> List[dict]:
        raise NotImplementedError


class StorageInterface(ABC):
    @abstractmethod
    def get_url_id_or_create(self, url: str) -> Optional[int]:
        raise NotImplementedError

    @abstractmethod
    def save_encoding(
        self,
        url_id: int,
        ts: float,
        face_id: int,
        box: List[int],
        entity: str,
        entity_id: int,
        tags: List[str],
        encoder: str,
        encoding: np.ndarray,
    ) -> int:
        raise NotImplementedError


def is_url(url: str) -> bool:
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
        storage: StorageInterface,
    ):
        self.downloader = downloader
        self.retriever = retriever
        self.resizer = resizer
        self.detector = detector
        self.publisher = publisher
        self.storage = storage

    def download(self, url: str) -> dict:
        return self.downloader.download(url).__dict__

    def retrieve(
        self,
        url: str,
        resize_height: int = None,
        number_of_upsamples: int = 0,
        locate_model: str = "fog",
        num_jitters: int = 1,
        encode_model: str = "small",
        tolerance: float = 0.6,
    ) -> List[dict]:
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
            tolerance (float, optional): How much distance between faces to consider it a match. Lower is more strict.
                0.6 is typical best performance.
        """
        filename = self.get_file_path(url)
        if filename is None:
            return [{"success": False, "resolution": f"File [{url}] not found"}]

        faces = self.get_faces(
            filename, resize_height, number_of_upsamples, locate_model, num_jitters, encode_model, tolerance
        )
        logging.info(f"{len(faces)} faces found")

        return self.publisher.publish(faces, path.realpath(path.dirname(filename)))

    def memorize(
        self,
        url: str,
        type: str,
        entity: str,
        id: str,
        tags: List[str],
        tolerance: float = 0.45,
    ):
        url_id: int = self.storage.get_url_id_or_create(url)
        logging.info(f"URL ID: {url_id}")

        filename = self.get_file_path(url)
        if filename is None:
            return [{"success": False, "resolution": f"File [{url}] not found"}]

        faces = self.get_faces(filename=filename, tolerance=tolerance)
        logging.info(f"{len(faces)} faces found")

        print(faces)
        # Here we need to save the url, embedding with url_id, faces content and send info about saved data.
        encodings_ids = []
        for face in faces:
            box = list((face.box["top"], face.box["right"], face.box["bottom"], face.box["left"]))
            encodings_ids.append(
                self.storage.save_encoding(
                    url_id, face.ts, face.id, box, entity, id, list([tags]), "test", face.encoding
                )
            )

        return [{"success": True, "resolution": f"File [{url}] memorized successfully", "encodings": encodings_ids}]

    def get_faces(
        self,
        filename: str,
        resize_height: int = None,
        number_of_upsamples: int = 0,
        locate_model: str = "fog",
        num_jitters: int = 1,
        encode_model: str = "small",
        tolerance: float = 0.6,
    ) -> List[DetectedFaceResponse]:
        frames: List[RetrievedFrameResponse] = self.retriever.retrieve(filename)
        logging.info(f"{len(frames)} frames retrieved from video file")

        if resize_height is not None:
            frames = self.resizer.resize(frames, resize_height)
            logging.info(f"{len(frames)} frames resized to height {resize_height}")

        return self.detector.detect(frames, number_of_upsamples, locate_model, num_jitters, encode_model, tolerance)

    def get_file_path(self, url: str) -> str:
        if is_url(url):
            return self.downloader.download(url).path

        if path.exists(url):
            return url

        raise MediaGrabberError(f"File {url} not found (not URL or existing file)")
