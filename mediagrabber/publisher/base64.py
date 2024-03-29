from typing import List
from mediagrabber.core import DetectedFaceResponse, FacesPublisherInterface
from io import BytesIO
from base64 import b64encode
from PIL.Image import Image


class Base64FacePublisher(FacesPublisherInterface):
    """
    Returns faces encoded into the base64 in the list of dictionaries.

    Args:
        FacesPublisherInterface ([List[DetectedFaceResponse]]): The faces list
    """

    def publish(self, faces: List[DetectedFaceResponse], directory: str) -> List[dict]:
        messages = []
        for face in faces:
            assert isinstance(face, DetectedFaceResponse)
            messages.append(
                {
                    "contentBase64": self.convert_image_to_base64(face.img),
                    "ts": face.ts,
                    "pts": face.pts,
                    "box": face.box,
                    "success": True,
                }
            )

        return messages

    def convert_image_to_base64(self, img: Image) -> str:
        """ Convert PIL Image to the string, using the base64 encoder

        Args:
            img (Image):  PIL Image

        Returns:
            str: Base64 encoded string with image content
        """
        buffer = BytesIO()
        img.save(buffer, format="webp")
        return "data:image/webp;base64," + b64encode(buffer.getvalue()).decode()
