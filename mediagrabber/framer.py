# The OpencvVideoFramesRetriever is an implementation of the `VideoFramesRetrieverInterface`
# based on the `youtube-dl` library for video downloading and `opencv` for frames retrieving
from typing import List
from mediagrabber import VideoFramesRetrieverInterface, MediaGrabberError
import youtube_dl
import subprocess
import datetime
import os
import cv2
import hashlib


class OpencvVideoFramesRetriever(VideoFramesRetrieverInterface):
    workdir: str

    def __init__(self, workdir: str):
        self.workdir = workdir
        print('Workdir: ' + workdir)

    def download_video(self, video_page_url: str) -> str:
        """
        Downloads videos from the specified page and stores the file in the `workdirectory`
        Returns the full path to the downloaded video file.
        """
        video_directory = self.create_video_directory(video_page_url)
        path = os.path.join(video_directory, 'source.mp4')
        args = ['youtube-dl', '-f', 'bestvideo[height<=480]+bestaudio/best[height<=480]', video_page_url, '-o', path]
        retcode = subprocess.call(args)
        if retcode > 0:
            raise MediaGrabberError("Video downloading failed")

        return path

    def create_video_directory(self, video_page_url) -> str:
        video_directory = os.path.join(self.workdir, hashlib.md5(
            str(video_page_url).encode('utf-8')).hexdigest())

        try:
            os.mkdir(video_directory)
        except FileExistsError:
            pass

        return video_directory

    def get_frames(self, video_page_url: str) -> List[bytes]:
        video_file_path = self.download_video(video_page_url)
        frames_dir = os.path.dirname(video_file_path)
        print('Frames directory: ' + frames_dir)
        start = datetime.datetime.now()
        # extract_frames(video_file_path, frames_dir)
        frames = filter_frames(retrieve_frames(video_file_path))
        save_frames(frames, os.path.dirname(video_file_path))
        print('Duration for ' + str(len(frames)) + ' frames retrieving:')
        print(datetime.datetime.now() - start)
        return []

    @staticmethod
    def get_video_url(video_page_url: str) -> str:
        opts = {format: 'bestvideo[height<=480]+bestaudio/best[height<=480]'}
        ydl = youtube_dl.YoutubeDL(opts)
        meta = ydl.extract_info(video_page_url, download=False)
        return meta['url']


def get_image_difference(image_1, image_2):
    first_image_hist = cv2.calcHist([image_1], [0], None, [256], [0, 256])
    second_image_hist = cv2.calcHist([image_2], [0], None, [256], [0, 256])

    img_hist_diff = cv2.compareHist(
        first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA)
    img_template_probability_match = cv2.matchTemplate(
        first_image_hist, second_image_hist, cv2.TM_CCOEFF_NORMED)[0][0]
    img_template_diff = 1 - img_template_probability_match

    # taking only 10% of histogram diff, since it's less accurate than template method
    commutative_image_diff = (img_hist_diff / 10) + img_template_diff
    return commutative_image_diff


def retrieve_frames(video_file_path) -> List:
    capture = cv2.VideoCapture(video_file_path)  # open the video using OpenCV
    imgs: List = []
    success, img = capture.read()
    while success:
        imgs.append(img)
        success, img = capture.read()

    return imgs

def filter_frames(frames: List):
    filtered_frames = []
    current_frame = None
    for frame in frames:
        if current_frame is None:
            current_frame = frame
        else:
            diff = get_image_difference(current_frame, frame)
            # print('Images difference is ' + str(diff))
            current_frame = frame
            if diff >= 0.5:
                filtered_frames.append(frame)

    return filtered_frames

def save_frames(frames: List, path: str) -> None:
    for i, frame in enumerate(frames):
        save_path = os.path.join(path, "{:010d}.jpg".format(i))
        cv2.imwrite(save_path, image)


def extract_frames(video_path, frames_dir):
    capture = cv2.VideoCapture(video_path)  # open the video using OpenCV
    if end < 0:  # if end isn't specified assume the end of the video
        end = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    capture.set(1, start)  # set the starting frame of the capture
    frame = start  # keep track of which frame we are up to, starting from start
    # a safety counter to ensure we don't enter an infinite while loop (hopefully we won't need it)
    while_safety = 0
    saved_count = 0  # a count of how many frames we have saved

    current_image = None

    while frame < end:  # lets loop through the frames until the end

        _, image = capture.read()  # read an image from the capture

        if while_safety > 500:  # break the while if our safety maxs out at 500
            break

        # sometimes OpenCV reads None's during a video, in which case we want to just skip
        if image is None:  # if we get a bad return flag or the image we read is None, lets not save
            # add 1 to our while safety, since we skip before incrementing our frame variable
            while_safety += 1
            continue  # skip

        if current_image is None:
            current_image = image
        else:
            diff = get_image_difference(current_image, image)
            # print('Images difference is ' + str(diff))
            current_image = image
            if diff < 0.5:
                continue

        if frame % every == 0:  # if this is a frame we want to write out based on the 'every' argument
            while_safety = 0  # reset the safety count
            # create the save path
            save_path = os.path.join(frames_dir, "{:010d}.jpg".format(frame))
            print('save path: ' + save_path)
            # if it doesn't exist or we want to overwrite anyways
            if not os.path.exists(save_path) or overwrite:
                # save the extracted image
                saved = cv2.imwrite(save_path, image)
                if not saved:
                    print("Can not write to [" + save_path + "]")
                saved_count += 1  # increment our counter by one

        frame += 1  # increment our frame count

    capture.release()  # after the while has finished close the capture

    return saved_count  # and return the count of the images we saved


# url = 'https://abcnews.go.com/Technology/video/garmin-outage-affects-millions-72012069'
url = 'https://abcnews.go.com/Technology/video/california-judge-orders-uber-lyft-reclassify-drivers-employees-72302309'
# url = 'https://rt.pornhub.com/view_video.php?viewkey=ph5e594b0eae0c8'

f = OpencvVideoFramesRetriever(os.path.realpath('workdir'))
frames = f.get_frames(url)

print(frames)
