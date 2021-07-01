from mediagrabber.downloader.ytdlp import YtdlpVideoDownloader
from mediagrabber.downloader.direct import DirectMediaDownloader
from mediagrabber.downloader.youtubedl import YoutubedlVideoDownloader
from mediagrabber.core import MediaDownloaderInterface, MediaDownloaderFactoryInterface, MediaGrabberError


class MediaDownloaderFactory(MediaDownloaderFactoryInterface):
    def __init__(self, workdir: str) -> None:
        self.workdir = workdir

    def get_media_downloader(self, id: str) -> MediaDownloaderInterface:
        if id == "youtubedl":
            return YoutubedlVideoDownloader(self.workdir)

        if id == "ytdlp":
            return YtdlpVideoDownloader(self.workdir)

        if id == "direct":
            return DirectMediaDownloader(self.workdir)

        msg = f"Unknown downloader: [{id}]. Supported downloaders: youtubedl, ytdlp, direct"
        raise MediaGrabberError({"message": msg})
