from typing import List
from mediagrabber.downloader.youtubedl import YoutubedlVideoDownloader


class YtdlpVideoDownloader(YoutubedlVideoDownloader):
    def create_download_command(self, url: str, path: str, quality: int) -> List[str]:
        return [
            "yt-dlp",
            "-f",
            f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]",
            url,
            "-o",
            path,
            "--external-downloader",
            "aria2c",
            "--external-downloader-args",
            "'-j 16 -s 16 -x 16 -k 5M'",
            "--no-playlist",
        ]
