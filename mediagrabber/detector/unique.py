from typing import List
from mediagrabber.core import FacesDetectorInterface, DetectedFaceResponse
from PIL.Image import Image
from tqdm import tqdm
import face_recognition
import numpy as np


class UniqueFaceDetector(FacesDetectorInterface):
    known_encodings: List[np.array] = []

    def detect(
        self,
        frames: List[Image],
        number_of_upsamples: int = 0,
        locate_model: str = "fog",
        num_jitters: int = 1,
        encode_model: str = "small",
        tolerance: float = 0.6,
    ) -> List[DetectedFaceResponse]:
        print(f"Tolerance: {tolerance}")
        detected_faces: List[DetectedFaceResponse] = []
        for i, frame in enumerate(tqdm(frames, "Faces detection")):
            frame_data = np.array(frame)
            locations = face_recognition.face_locations(frame_data, number_of_upsamples, locate_model)
            encodings = face_recognition.face_encodings(frame_data, locations, num_jitters, encode_model)

            j = 0
            for (top, right, bottom, left), encoding in zip(locations, encodings):
                if self.is_known(encoding, tolerance):
                    # Face already is found and should be skipped
                    continue

                # Crop the face from frame and add to results
                face = frame.crop(box=(left, top, right, bottom))
                detected_faces.append(DetectedFaceResponse(f"face-{i}-{j}", face))
                j += 1

            # @TODO Add frame saving if it is required

        return detected_faces

    def is_known(self, encoding: np.array, tolerance: float) -> bool:
        results = face_recognition.compare_faces(self.known_encodings, encoding, tolerance)
        if True in results:
            return True

        self.known_encodings.append(encoding)
        return False
