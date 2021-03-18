from typing import List
from mediagrabber.core import DetectedFaceResponse, FacesPublisherInterface
from os import path

class FileFacePublisher(FacesPublisherInterface):
    """
    Saved faces to the specified directory

    Args:
        FacesPublisherInterface ([List[DetectedFaceResponse]]): The faces list
    """
    def publish(self, faces: List[DetectedFaceResponse], directory: str) -> List[dict]:
        filenames = []
        for face in faces:
            filename: str = path.join(directory, face.id + '.png')
            face.img.save(filename)
            filenames.append(filename)

        return filenames
