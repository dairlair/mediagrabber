from abc import ABC, abstractmethod
from typing import Callable, List
from injector import inject
from io import BytesIO


class StorageInterface(ABC):
    @abstractmethod
    def save(self, content: bytes, name: str) -> str:
        raise NotImplementedError


class VideoFramesRetrieverInterface(ABC):
    @abstractmethod
    def get_frames(self, video_page_url: str) -> List[bytes]:
        raise NotImplementedError


class MediaGrabber(ABC):
    @inject
    def __init__(self, video_frames_retriever: VideoFramesRetrieverInterface, storage: StorageInterface):
        self.video_frames_retriever = video_frames_retriever
        self.storage = storage

    def grab(self, url: str) -> List[str]:
        print(f"Start URL processing: {url}")
        frames = self.video_frames_retriever.get_frames(url)
        frame_urls: List[str] = []
        for i, content in enumerate(frames):
            name = f"{url}-{i}"
            frame_url = self.storage.save(content, name)
            frame_urls.append(frame_url)

        return frame_urls