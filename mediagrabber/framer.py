# The Frames is an implementation of the `VideoFramesRetrieverInterface`
# based on the `youtube-dl` library.
from typing import List
from mediagrabber import VideoFramesRetrieverInterface

class Framer(VideoFramesRetrieverInterface):
    def get_frames(self, url: str) -> List[bytes]:
        print ('Start frames extracting...')
        return []


url = 'https://abcnews.go.com/Technology/video/garmin-outage-affects-millions-72012069'
f = Framer()
frames = f.get_frames(url)

print(frames)
