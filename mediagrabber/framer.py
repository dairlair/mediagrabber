# The OpencvVideoFramesRetriever is an implementation
# of the `VideoFramesRetrieverInterface`
# based on the `youtube-dl` library for video downloading and `opencv`
# for frames retrieving
# How to use:
# ```python
#   url = 'https://abcnews.go.com/Technology/video/california-judge-orders-uber-lyft-reclassify-drivers-employees-72302309'
#   frames = OpencvVideoFramesRetriever('/tmp')
# ````


from mediagrabber.meter.meter import MeterInterface, Metric
from typing import List
from abc import ABC, abstractmethod
from mediagrabber.core import FramerInterface, MediaGrabberError
import os
import cv2
import logging
import shutil


class VideoDownloadedResponse(object):
    size: int = None

    def __init__(self, code: int, output: str, path: str, duration: str):
        self.code = code
        self.output = output
        self.path = path
        self.duration = duration
        self.size = os.path.getsize(path)


class VideoDownloaderInterface(ABC):
    @abstractmethod
    def download(self, workdir: str, video_page_url: str) -> VideoDownloadedResponse:
        raise NotImplementedError


class OpencvVideoFramesRetriever(FramerInterface):
    workdir: str
    downloader: VideoDownloaderInterface
    meter: MeterInterface

    def __init__(
        self,
        workdir: str,
        downloader: VideoDownloaderInterface,
        meter: MeterInterface,
    ):
        self.workdir = workdir
        self.downloader = downloader
        self.meter = meter

    def get_frames(self, video_page_url: str) -> List[bytes]:
        vdl: VideoDownloadedResponse = self.download(video_page_url)
        logging.info(f"Video downloaded at {vdl.path}")

        frames = self.retrieve_frames(vdl)
        frames = self.filter_frames(frames)
        directory = os.path.dirname(vdl.path)
        result = self.save_frames(frames, directory)

        shutil.rmtree(directory)

        return result

    def download(self, video_page_url: str) -> VideoDownloadedResponse:
        def fn():
            return self.downloader.download(self.workdir, video_page_url)

        metric: Metric
        vdl: VideoDownloadedResponse
        (metric, vdl) = self.meter.calculate_metric('media_grabbed', fn)
        if vdl.code != 0 or vdl.path is None:
            raise MediaGrabberError(vdl.__dict__)

        metric.fields['size'] = vdl.size
        self.meter.write_metric(metric)

        return vdl

    def retrieve_frames(self, vdl: VideoDownloadedResponse) -> List:
        def fn() -> List[any]:
            return retrieve_frames(vdl.path)

        (metric, frames) = self.meter.calculate_metric('frames_retrieved', fn)   
        metric.fields['size'] = vdl.size
        metric.fields['count'] = len(frames)
        self.meter.write_metric(metric)

        return frames

    def filter_frames(self, frames: List) -> List:
        def fn() -> List[any]:
            return filter_frames(frames)

        (metric, frames) = self.meter.calculate_metric('frames_filtered', fn)
        metric.fields['count'] = len(frames)
        self.meter.write_metric(metric)

        return frames

    def save_frames(self, frames: List, path: str) -> List[bytes]:
        def fn() -> List[bytes]:
            return save_frames(frames, path)

        (metric, frames) = self.meter.calculate_metric('frames_saved', fn)
        metric.fields['count'] = len(frames)
        self.meter.write_metric(metric)

        return frames


def get_image_difference(image_1, image_2):
    first_image_hist = cv2.calcHist([image_1], [0], None, [256], [0, 256])
    second_image_hist = cv2.calcHist([image_2], [0], None, [256], [0, 256])

    img_hist_diff = cv2.compareHist(first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA)
    img_template_probability_match = cv2.matchTemplate(first_image_hist, second_image_hist, cv2.TM_CCOEFF_NORMED)[0][0]
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


def filter_frames(frames: List) -> List:
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
