# The OpencvVideoFramesRetriever is an implementation
# of the `VideoFramesRetrieverInterface`
# based on the `youtube-dl` library for video downloading and `opencv`
# for frames retrieving
# How to use:
# ```python
#   url = 'https://abcnews.go.com/Technology/video/california-judge-orders-uber-lyft-reclassify-drivers-employees-72302309'
#   frames = OpencvVideoFramesRetriever('/tmp')
# ````


from typing import List
from abc import ABC, abstractmethod
from mediagrabber.core import FramerInterface, MediaGrabberError
import os
import cv2
import logging


class VideoDownloadedResponse(object):
    def __init__(self, code: int, output: str, path: str, duration: str):
        self.code = code
        self.output = output
        self.path = path
        self.duration = duration


class VideoDownloaderInterface(ABC):
    @abstractmethod
    def download(
        self, workdir: str, video_page_url: str
    ) -> VideoDownloadedResponse:
        raise NotImplementedError


class OpencvVideoFramesRetriever(FramerInterface):
    workdir: str
    downloader: VideoDownloaderInterface

    def __init__(self, workdir: str, downloader: VideoDownloaderInterface):
        self.workdir = workdir
        self.downloader = downloader

    def get_frames(self, video_page_url: str) -> List[bytes]:
        response = self.downloader.download(self.workdir, video_page_url)
        if response.code != 0 or response.path is None:
            raise MediaGrabberError(response.__dict__)

        path = response.path
        logging.info(f"Video downloaded at {path}")
        frames = filter_frames(retrieve_frames(path))
        return save_frames(frames, os.path.dirname(path))


def get_image_difference(image_1, image_2):
    first_image_hist = cv2.calcHist([image_1], [0], None, [256], [0, 256])
    second_image_hist = cv2.calcHist([image_2], [0], None, [256], [0, 256])

    img_hist_diff = cv2.compareHist(
        first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA
    )
    img_template_probability_match = cv2.matchTemplate(
        first_image_hist, second_image_hist, cv2.TM_CCOEFF_NORMED
    )[0][0]
    img_template_diff = 1 - img_template_probability_match

    # taking only 10% of histogram diff,
    # since it's less accurate than template method
    commutative_image_diff = (img_hist_diff / 10) + img_template_diff
    return commutative_image_diff


def retrieve_frames(video_file_path) -> List:
    capture = cv2.VideoCapture(video_file_path)  # open the video using OpenCV
    fps = round(capture.get(cv2.CAP_PROP_FPS))
    imgs: List = []
    success, img = capture.read()

    i = 0
    while success:
        if i % fps == 0:
            imgs.append(img)

        success, img = capture.read()
        i += 1

    capture.release()

    return imgs


def filter_frames(frames: List):
    scored = []
    current_frame = None
    for frame in frames:
        diff = get_image_difference(current_frame, frame)
        scored.append((diff, frame))
        current_frame = frame

    return [item[1] for item in filter(lambda x: x[0] >= 0.5, scored)]


def save_frames(frames: List, path: str) -> List[bytes]:
    frames_data: List[bytes] = []
    for i, frame in enumerate(frames):
        save_path = os.path.join(path, "{:010d}.jpg".format(i))
        cv2.imwrite(save_path, frame)
        with open(save_path, "rb") as input:
            frames_data.append(input.read())

    return frames_data
