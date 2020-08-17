# The Frames is an implementation of the `VideoFramesRetrieverInterface`
# based on the `youtube-dl` library.
from typing import List
from mediagrabber import VideoFramesRetrieverInterface
import youtube_dl
import subprocess
import datetime
import os
import cv2

class Framer(VideoFramesRetrieverInterface):
    def get_frames(self, video_page_url: str) -> List[bytes]:
        subprocess.call(['youtube-dl', '-f', 'bestvideo[height<=480]+bestaudio/best[height<=480]', video_page_url, '-o', "movie.mp4"])
        print ('Downloaded')
        start = datetime.datetime.now()
        extract_frames('movie.mp4', './frames')
        print('Duration:')
        print(datetime.datetime.now() - start)
        # url: str = self.get_video_url(video_page_url)
        # print('Video URL: [' + url + ']')
        return []

    @staticmethod
    def get_video_url(video_page_url: str) -> str:
        opts = {format: 'bestvideo[height<=480]+bestaudio/best[height<=480]'}
        ydl = youtube_dl.YoutubeDL(opts)
        meta = ydl.extract_info(video_page_url, download=False)
        return meta['url']


def extract_frames(video_path, frames_dir, overwrite=False, start=-1, end=-1, every=1):
    """
    Extract frames from a video using OpenCVs VideoCapture
    :param video_path: path of the video
    :param frames_dir: the directory to save the frames
    :param overwrite: to overwrite frames that already exist?
    :param start: start frame
    :param end: end frame
    :param every: frame spacing
    :return: count of images saved
    """

    video_path = os.path.normpath(video_path)  # make the paths OS (Windows) compatible
    frames_dir = os.path.normpath(frames_dir)  # make the paths OS (Windows) compatible

    video_dir, video_filename = os.path.split(video_path)  # get the video path and filename from the path

    assert os.path.exists(video_path)  # assert the video file exists

    capture = cv2.VideoCapture(video_path)  # open the video using OpenCV

    if start < 0:  # if start isn't specified lets assume 0
        start = 0
    if end < 0:  # if end isn't specified assume the end of the video
        end = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    capture.set(1, start)  # set the starting frame of the capture
    frame = start  # keep track of which frame we are up to, starting from start
    while_safety = 0  # a safety counter to ensure we don't enter an infinite while loop (hopefully we won't need it)
    saved_count = 0  # a count of how many frames we have saved

    while frame < end:  # lets loop through the frames until the end

        _, image = capture.read()  # read an image from the capture

        if while_safety > 500:  # break the while if our safety maxs out at 500
            break

        # sometimes OpenCV reads None's during a video, in which case we want to just skip
        if image is None:  # if we get a bad return flag or the image we read is None, lets not save
            while_safety += 1  # add 1 to our while safety, since we skip before incrementing our frame variable
            continue  # skip

        if frame % every == 0:  # if this is a frame we want to write out based on the 'every' argument
            while_safety = 0  # reset the safety count
            save_path = os.path.join(frames_dir, video_filename, "{:010d}.jpg".format(frame))  # create the save path
            if not os.path.exists(save_path) or overwrite:  # if it doesn't exist or we want to overwrite anyways
                cv2.imwrite(save_path, image)  # save the extracted image
                saved_count += 1  # increment our counter by one

        frame += 1  # increment our frame count

    capture.release()  # after the while has finished close the capture

    return saved_count  # and return the count of the images we saved



url = 'https://abcnews.go.com/Technology/video/garmin-outage-affects-millions-72012069'
f = Framer()
frames = f.get_frames(url)

print(frames)
