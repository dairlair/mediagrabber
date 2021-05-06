from mediagrabber.retriever.pil import PilFramesRetriever
from mediagrabber.core import FramesRetrieverInterface, FramesRetrieverFactoryInterface
from mediagrabber.retriever.av import AvFramesRetriever
import filetype

class FramesRetrieverFactory(FramesRetrieverFactoryInterface):
    def get_frames_retriever(self, file: str) -> FramesRetrieverInterface:
        kind = filetype.guess(file)
        if kind is None:
            raise ValueError(f"Cannot guess file type: [{file}]")

        format = kind.mime.split('/')[0]
        if format == 'video':
            return AvFramesRetriever()

        if format == 'image':
            return PilFramesRetriever()

        raise NotImplementedError(f"Not supported file type [{kind.mime}]")

    