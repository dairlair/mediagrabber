from typing import List
from mediagrabber.core import DetectedFaceResponse, FacesPublisherInterface
from io import BytesIO
from base64 import b64encode


class Base64FacePublisher(FacesPublisherInterface):
    """
    Returns faces encoded into the base64 in the list of dictionaries.

    Args:
        FacesPublisherInterface ([List[DetectedFaceResponse]]): The faces list
    """

    def publish(self, faces: List[DetectedFaceResponse], directory: str) -> List[dict]:
        messages = []
        for face in faces:
            buffer = BytesIO()
            face.img.save(buffer, format="jpeg")
            content_base_64 = "data:image/jpeg;base64," + b64encode(buffer.getvalue()).decode()
            messages.append({"contentBase64": content_base_64})

        return messages
