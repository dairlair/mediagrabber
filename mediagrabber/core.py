from abc import ABC, abstractmethod
from dataclasses import dataclass
import logging
from mediagrabber.storage.model.face import Face
from os import path
from typing import List, Optional
from PIL.Image import Image
from injector import inject
import os
import numpy as np


@dataclass
class MediaGrabberError(Exception):
    data: dict


class DownloadedMediaResponse:
    size: int = None

    def __init__(self, code: int, output: str, path: str, duration: str):
        self.code = code
        self.output = output
        self.path = path
        self.duration = duration
        if path is not None:
            self.size = os.path.getsize(path)


class MediaDownloaderInterface(ABC):
    @abstractmethod
    def download(self, url: str) -> DownloadedMediaResponse:
        raise NotImplementedError


class MediaDownloaderFactoryInterface(ABC):
    @abstractmethod
    def get_media_downloader(self, id: str) -> MediaDownloaderInterface:
        raise NotImplementedError


@dataclass
class RetrievedFrameResponse:
    ts: float
    pts: int
    img: Image


class FramesRetrieverInterface(ABC):
    @abstractmethod
    def retrieve(self, file: str) -> List[RetrievedFrameResponse]:
        """Reads the media file and retrieves frames in the Pillow library format.

        Args:
            file (str): Path to the file

        Returns:
            List[RetrievedFrameResponse]: List of the retrieved frames
        """
        raise NotImplementedError


class FramesRetrieverFactoryInterface(ABC):
    @abstractmethod
    def get_frames_retriever(self, file: str) -> FramesRetrieverInterface:
        """Detects local file type and returns suitable frames retriever

        Args:
            file (str): Filename

        Returns:
            FramesRetrieverInterface:
        """
        raise NotImplementedError


class FramesResizerInterface(ABC):
    @abstractmethod
    def resize(self, frames: List[RetrievedFrameResponse], height: int = 360) -> List[RetrievedFrameResponse]:
        raise NotImplementedError


@dataclass
class DetectedFaceResponse:
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
        number_of_upsamples: int = 1,
        locate_model: str = "fog",
        num_jitters: int = 1,
        encode_model: str = "small",
        tolerance: float = 0.6,
    ) -> List[DetectedFaceResponse]:
        raise NotImplementedError

    @abstractmethod
    def get_id(self) -> str:
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
        urlId: int,
        ts: float,
        box: List[int],
        entity: str,
        entityId: int,
        tags: List[str],
        encoder: str,
        encoding: np.ndarray,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_faces() -> List[Face]:
        raise NotImplementedError


@dataclass
class FaceDistance:
    faceId: int
    distance: float

class DistancerInterface(ABC):
    def __init__(self, storage: StorageInterface) -> None:
        self.storage = storage

    def get_nns_by_face_id(self, faceId: int, n: int, tags: List[str]) -> List[FaceDistance]:
        raise NotImplementedError


def is_url(url: str) -> bool:
    return url.startswith(("http://", "https://"))


class MediaGrabber(ABC):
    @inject
    def __init__(
        self,
        retriever_factory: FramesRetrieverFactoryInterface,
        resizer: FramesResizerInterface,
        detector: FacesDetectorInterface,
        publisher: FacesPublisherInterface,
        storage: StorageInterface,
        downloader_factory: MediaDownloaderFactoryInterface,
        distancer: DistancerInterface,
    ):
        self.retriever_factory = retriever_factory
        self.resizer = resizer
        self.detector = detector
        self.publisher = publisher
        self.storage = storage
        self.downloader_factory = downloader_factory
        self.distancer = distancer

    def download(self, url: str, source: str = "youtubedl") -> dict:
        return self.downloader_factory.get_media_downloader(source).download(url).__dict__

    def retrieve(
        self,
        url: str,
        source: str,
        resize_height: int = None,
        number_of_upsamples: int = 1,
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
        filename = self.get_file_path(url, source)
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
        source: str = "youtubedl",  # @TODO Implement photos support by the direct URL
        entity: str = "default",
        id: str = 0,
        tags: List[str] = list(),
        tolerance: float = 0.45,
    ) -> List[dict]:
        """Retrieves faces from the file and memorize thems into the database.

        Args:
            url (str): URL or path to file.
            source (str): video or photo. Should be used for downloader factory using.
            entity (str): The name of entity (used for external linkage).
            id (str): [description] The id of entity (used for external linkage).
            tags (List[str]): The tags, which are associated with the file. Used for further recognition.
            tolerance (float, optional): How much distance between faces to consider it a match. Lower is more strict.
                0.6 is typical best performance. Defaults to 0.45.

        Returns:
            [List[dict]]: Returns information about memorized faces.
        """
        urlId: int = self.storage.get_url_id_or_create(url)
        logging.info(f"URL ID: {urlId}")

        filename = self.get_file_path(url, source)
        if filename is None:
            return [{"success": False, "resolution": f"File [{url}] not found"}]

        faces = self.get_faces(filename=filename, tolerance=tolerance)
        logging.info(f"{len(faces)} faces found")

        encodings_ids = []
        for face in faces:
            box = list((face.box["top"], face.box["right"], face.box["bottom"], face.box["left"]))
            tags = prepare_tags(tags)
            encodings_ids.append(
                self.storage.save_encoding(
                    urlId, face.ts, box, entity, id, tags, self.detector.get_id(), face.encoding
                )
            )

        return [{"success": True, "resolution": f"File [{url}] memorized successfully", "faces": encodings_ids}]

    def recognize(self, faceId: int, count: int = 10, tags: List[str] = list()) -> dict:
        # @TODO Implement face existense check
        tags = prepare_tags(tags)
        distances = self.distancer.get_nns_by_face_id(faceId, count, tags)
        return [{"success": True, "faces": [x.__dict__ for x in distances]}]

    def get_faces(
        self,
        filename: str,
        resize_height: int = None,
        number_of_upsamples: int = 1,
        locate_model: str = "fog",
        num_jitters: int = 1,
        encode_model: str = "small",
        tolerance: float = 0.6,
    ) -> List[DetectedFaceResponse]:
        frames: List[RetrievedFrameResponse] = self.retriever_factory.get_frames_retriever(filename).retrieve(filename)
        logging.info(f"{len(frames)} frames retrieved from media file")

        if resize_height is not None:
            frames = self.resizer.resize(frames, resize_height)
            logging.info(f"{len(frames)} frames resized to height {resize_height}")

        return self.detector.detect(frames, number_of_upsamples, locate_model, num_jitters, encode_model, tolerance)

    def get_file_path(self, url: str, source: str = "direct") -> str:
        if is_url(url):
            downloader: MediaDownloaderInterface = self.downloader_factory.get_media_downloader(source)
            return downloader.download(url).path

        if path.exists(url):
            return url

        raise MediaGrabberError(f"File {url} not found (not URL or existing file)")


def prepare_tags(tags: List[str]) -> List[str]:
    if isinstance(tags, str):
        tags = list(tags.split(","))
    tags = list(tags)
    assert isinstance(tags, List)
    return tags
