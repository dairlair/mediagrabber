from abc import ABC, abstractmethod
from mediagrabber.meter.meter import MeterInterface, Metric
from typing import List
import hashlib
from injector import inject


class MediaGrabberError(Exception):
    """
    Just a general error for MediaGrabber
    """

    def __init__(self, data: dict):
        self.data = data


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
    meter: MeterInterface

    @inject
    def __init__(self, framer: FramerInterface, storage: StorageInterface, meter: MeterInterface):
        self.video_frames_retriever = framer
        self.storage = storage
        self.meter = meter

    """
    :raises: MediaGrabberError
    """

    def grab(self, url: str) -> List[str]:
        frames = self.video_frames_retriever.get_frames(url)
        frame_urls: List[str] = []
        hash = hashlib.md5(url.encode("utf-8")).hexdigest()
        for i, content in enumerate(frames):
            name = f"{hash}-{i}.jpg"

            frame_url = self.save(content, name)

            frame_urls.append(frame_url)

        return frame_urls

    def save(self, content: bytes, name: str) -> str:
        def fn():
            return self.storage.save(content, name)

        return self.meter.measure('operation', fn, {'type': 'file_uploaded_to_object_storage'}, {'size': len(content)})
