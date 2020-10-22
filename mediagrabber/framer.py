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
from mediagrabber.core import FramerInterface, MediaGrabberError
import subprocess
import os
import cv2
import hashlib
import glob
import logging


# @TODO Move video downloader to another dependency
class DownloadVideoResponse(object):
    def __init__(
        self,
        return_code: int,
        stdout: str,
        stderr: str,
        path: str,
        duration: str,
    ):
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr
        self.path = path
        self.duration = duration


class OpencvVideoFramesRetriever(FramerInterface):
    workdir: str

    def __init__(self, workdir: str):
        self.workdir = workdir

    def get_frames(self, video_page_url: str) -> List[bytes]:
        response = self.download_video(video_page_url)
        path = response.path
        logging.info(f"Video downloaded at {path}")
        frames = filter_frames(retrieve_frames(path))
        return save_frames(frames, os.path.dirname(path))

    def download_video(self, video_page_url: str) -> DownloadVideoResponse:
        """
        Downloads videos from the specified page and stores the file
        in the `workdirectory`.
        Returns the full path to the downloaded video file.
        """
        video_directory = self.create_video_directory(video_page_url)
        path = os.path.join(video_directory, "source.%(ext)s")
        command = [
            "youtube-dl",
            "-f",
            "bestvideo[height<=480]+bestaudio/best[height<=480]",
            video_page_url,
            "-o",
            path,
        ]

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        (stdout, stderr) = process.communicate()

        # Wait for date to terminate. Get return returncode ##
        return_code = process.wait()
        if return_code != 0:
            return DownloadVideoResponse(
                return_code, stdout, stderr, None, None
            )

        # Try to find downloadded file
        mask = os.path.join(video_directory, "source.*")
        path = next(iter(glob.glob(mask)), None)
        if not path or not os.path.exists(path):
            raise MediaGrabberError("Video file donwloaded but not found")

        duration = parse_duration(stdout)

        return DownloadVideoResponse(
            return_code, stdout, stderr, str(path), duration
        )

    def create_video_directory(self, video_page_url: str) -> str:
        hash = hashlib.md5(video_page_url.encode("utf-8")).hexdigest()
        directory = os.path.join(self.workdir, hash)

        try:
            os.mkdir(directory)
        except FileExistsError:
            pass

        if os.access(directory, os.W_OK) is False:
            raise MediaGrabberError("Video directory is not writable")

        logging.debug("Video directory created", {"directory": directory})

        return directory


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


def parse_duration(output: str) -> str:
    """
    Parses duration from youtube-dl output, like a
    "[download] 100.0% of 58.68MiB at 188.13KiB/s ETA 00:00\n[download] 100% of 58.68MiB in 05:20\n"
    and returns duration, e.g: "58.68MiB in 05:20"
    """
    return ""
