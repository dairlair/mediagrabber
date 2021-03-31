from mediagrabber.downloader.direct import DirectMediaDownloader
from mediagrabber.downloader.youtubedl import YoutubedlVideoDownloader
from mediagrabber.core import MediaDownloaderInterface, MediaDownloaderFactoryInterface, MediaGrabberError

class MediaDownloaderFactory(MediaDownloaderFactoryInterface):
    def __init__(self, workdir: str) -> None:
        self.workdir = workdir

    def get_media_downloader(self, id: str) -> MediaDownloaderInterface:
        if id == 'youtubedl':
            return YoutubedlVideoDownloader(self.workdir)

        if id == 'direct':
            return DirectMediaDownloader(self.workdir)

        raise MediaGrabberError({"message": f"Unknown downloader: [{id}]"})