from abc import ABC, abstractmethod
from typing import List
from injector import inject
import hashlib


class MediaGrabberError(Exception):
    """
        Just a general error for MediaGrabber
    """
    pass


class StorageInterface(ABC):
    @abstractmethod
    def save(self, content: bytes, name: str) -> str:
        raise NotImplementedError


class FramerInterface(ABC):
    @abstractmethod
    def get_frames(self, video_page_url: str) -> List[bytes]:
        raise NotImplementedError


class MediaGrabber(ABC):
    @inject
    def __init__(self, framer: FramerInterface, storage: StorageInterface):
        self.video_frames_retriever = framer
        self.storage = storage

    def grab(self, url: str) -> List[str]:
        print(f"Start URL processing: {url}")
        frames = self.video_frames_retriever.get_frames(url)
        frame_urls: List[str] = []
        hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        for i, content in enumerate(frames):
            name = f"{hash}-{i}.jpg"
            frame_url = self.storage.save(content, name)
            frame_urls.append(frame_url)

        return frame_urls
