from mediagrabber.core import MediaDownloaderInterface, DownloadedMediaResponse
import requests
import hashlib
import os


class DirectMediaDownloader(MediaDownloaderInterface):
    workdir: str

    def __init__(self, workdir: str) -> None:
        self.workdir = workdir

    def download(self, url: str) -> DownloadedMediaResponse:
        hash = hashlib.md5(url.encode("utf-8")).hexdigest()
        file = os.path.join(self.workdir, hash + ".jpg")

        with open(file, "wb") as f:
            r = requests.get(url, allow_redirects=True)
            f.write(r.content)

        return DownloadedMediaResponse(0, '', file, 0)
