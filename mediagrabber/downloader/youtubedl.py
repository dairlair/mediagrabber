from mediagrabber.framer import (
    VideoDownloaderInterface,
    VideoDownloadedResponse,
)
from mediagrabber.core import MediaGrabberError
import subprocess
import os
import glob
import hashlib
import logging
import threading


class SuperFile(threading.Thread):
    def __init__(self):
        super().__init__()
        self.readpipe, self.writepipe = os.pipe()

    def write(self, data):
        print("Data received")
        print(data)

    def fileno(self):
        # when fileno is called this indicates the subprocess is about to
        # fork => start thread
        return self.writepipe

    def finished(self):
        """If the write-filedescriptor is not closed this thread will
        prevent the whole program from exiting. You can use this method
        to clean up after the subprocess has terminated."""
        os.close(self.writepipe)

    def run(self):
        inputFile = os.fdopen(self.readpipe)

        while True:
            line = inputFile.readline()

            if len(line) == 0:
                #no new data was added
                break

            print(line)


class YoutubedlVideoDownloader(VideoDownloaderInterface):
    def download(
        self, workdir: str, video_page_url: str
    ) -> VideoDownloadedResponse:
        """
        Downloads videos from the specified page and stores the file
        in the `workdirectory`.
        Returns the full path to the downloaded video file.
        """
        video_directory = self.create_video_directory(workdir, video_page_url)
        path = os.path.join(video_directory, "source.%(ext)s")
        command = [
            "youtube-dl",
            "-f",
            "bestvideo[height<=480]+bestaudio/best[height<=480]",
            video_page_url,
            "-o",
            path,
        ]

        f = SuperFile()
        process = subprocess.Popen(command, stdout=f, stderr=f)

        (stdout, stderr) = process.communicate()

        # Wait for date to terminate. Get return returncode ##
        return_code = process.wait()
        if return_code != 0:
            return VideoDownloadedResponse(
                return_code, stdout, stderr, None, None
            )

        # Try to find downloadded file
        mask = os.path.join(video_directory, "source.*")
        path = next(iter(glob.glob(mask)), None)
        if not path or not os.path.exists(path):
            raise MediaGrabberError("Video file donwloaded but not found")

        duration = parse_duration(stdout)

        return VideoDownloadedResponse(
            return_code, stdout, stderr, str(path), duration
        )

    def create_video_directory(self, workdir: str, video_page_url: str) -> str:
        hash = hashlib.md5(video_page_url.encode("utf-8")).hexdigest()
        directory = os.path.join(workdir, hash)

        try:
            os.mkdir(directory)
        except FileExistsError:
            pass

        if os.access(directory, os.W_OK) is False:
            raise MediaGrabberError("Video directory is not writable")

        logging.debug("Video directory created", {"directory": directory})

        return directory


def parse_duration(output: str) -> str:
    """
    Parses duration from youtube-dl output, like a
    "[download] 100.0% of 58.68MiB at 188.13KiB/s ETA 00:00\n[download] 100% of 58.68MiB in 05:20\n"
    and returns duration, e.g: "58.68MiB in 05:20"
    """
    return ""
