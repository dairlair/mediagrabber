from mediagrabber.downloader.ytdlp import YtdlpVideoDownloader
from mediagrabber.downloader.direct import DirectMediaDownloader
from mediagrabber.downloader.youtubedl import YoutubedlVideoDownloader
from mediagrabber.core import MediaDownloaderInterface, MediaDownloaderFactoryInterface, MediaGrabberError
from enum import Enum

class DownloaderId(Enum):
    Direct = 'direct'
    YoutubeDL = 'youtubedl'
    YtDLP = 'ytdlp'


class MediaDownloaderFactory(MediaDownloaderFactoryInterface):
    def __init__(self, workdir: str) -> None:
        self.workdir = workdir

    def get_media_downloader(self, id: str) -> MediaDownloaderInterface:
        downloaders = {
            DownloaderId.Direct.value: DirectMediaDownloader(self.workdir),
            DownloaderId.YoutubeDL.value: YoutubedlVideoDownloader(self.workdir),
            DownloaderId.YtDLP.value: YtdlpVideoDownloader(self.workdir),
        }

        if id in downloaders:
            return downloaders[id]

        ids = ', '.join([id.value for id in DownloaderId])
        raise MediaGrabberError({"message": f"Unknown downloader: [{id}]. Supported downloaders: {ids}"})
