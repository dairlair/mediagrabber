from mediagrabber.core import VideoDownloaderInterface, DownloadedVideoResponse
from mediagrabber.core import MediaGrabberError
import subprocess
import os
import glob
import hashlib
import logging
import time
from pget.down import Downloader


class PgetVideoDownloader(VideoDownloaderInterface):
    workdir: str

    def __init__(self, workdir: str) -> None:
        self.workdir = workdir

    def download(self, video_page_url: str) -> DownloadedVideoResponse:
        """
        Downloads videos from the specified page and stores the file
        in the `workdirectory`.
        Returns the full path to the downloaded video file.
        """
        video_directory = self.create_video_directory(video_page_url)
        path = os.path.join(video_directory, "source.mp4")
        command = [
            "youtube-dl",
            "-f",
            "bestvideo[height<=360]+bestaudio/best[height<=360]",
            video_page_url,
            "--get-url"
            # "-o",
            # path,
        ]

        started_at = time.time()

        # started_at = time.time()
        # process = subprocess.Popen(
        #     command,
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.STDOUT,
        #     bufsize=1,
        #     universal_newlines=True,
        # )

        # output: str = ""
        # for line in process.stdout:
        #     logging.info(line)
        #     output += line

        # process.wait()

        # # Wait for date to terminate. Get return returncode ##
        # return_code = process.wait()
        # if return_code != 0:
        #     return DownloadedVideoResponse(return_code, output, None, None)

        # print(output)

        result = subprocess.run(command, stdout=subprocess.PIPE)
        url = result.stdout.rstrip()
        print(f"URL: {url}")

        downloader = Downloader(url, path, 16, high_speed=True)
        downloader.start()
        downloader.wait_for_finish()

        # Try to find downloadded file
        mask = os.path.join(video_directory, "source.*")
        path = next(iter(glob.glob(mask)), None)
        if not path or not os.path.exists(path):
            raise MediaGrabberError("Video file donwloaded but not found")

        duration = time.time() - started_at
        print(f"Duration: {duration}")

        return DownloadedVideoResponse(result.returncode, "", str(path), duration)

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
