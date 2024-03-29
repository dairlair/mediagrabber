from typing import List
from mediagrabber.core import MediaDownloaderInterface, DownloadedMediaResponse
from mediagrabber.core import MediaGrabberError
import subprocess
import os
import glob
import hashlib
import logging
import time


class YoutubedlVideoDownloader(MediaDownloaderInterface):
    workdir: str

    def __init__(self, workdir: str) -> None:
        self.workdir = workdir

    def create_download_command(self, url: str, path: str, quality: int) -> List[str]:
        return [
            "youtube-dl",
            "-f",
            f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]",
            url,
            "-o",
            path,
        ]

    def download(self, url: str, quality: int) -> DownloadedMediaResponse:
        """
        Downloads videos from the specified page and stores the file
        in the `workdirectory`.
        Returns the full path to the downloaded video file.
        """
        video_directory = self.create_video_directory(url)
        path = os.path.join(video_directory, "source.%(ext)s")
        command = self.create_download_command(url, path, quality)

        logging.info("Command to video download: " + ' '.join(command))

        started_at = time.time()
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True,
        )

        output: str = ""
        for line in process.stdout:
            logging.info(line)
            output += line

        process.wait()

        # Wait for date to terminate. Get return returncode ##
        return_code = process.wait()
        if return_code != 0:
            return DownloadedMediaResponse(return_code, output, None, None)

        # Try to find downloadded file
        mask = os.path.join(video_directory, "source.*")
        path = next(iter(glob.glob(mask)), None)
        if not path or not os.path.exists(path):
            raise MediaGrabberError("Video file donwloaded but not found")

        duration = time.time() - started_at

        return DownloadedMediaResponse(process.returncode, output, str(path), duration)

    def create_video_directory(self, url: str) -> str:
        hash = hashlib.md5(url.encode("utf-8")).hexdigest()
        directory = os.path.join(self.workdir, hash)

        try:
            os.mkdir(directory)
        except FileExistsError:
            pass

        if os.access(directory, os.W_OK) is False:
            raise MediaGrabberError("Video directory is not writable")

        logging.debug("Video directory created", {"directory": directory})

        return directory
