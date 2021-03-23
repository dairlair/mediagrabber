from typing import List
from mediagrabber.core import FacesDetectorInterface, DetectedFaceResponse, RetrievedFrameResponse
from tqdm import tqdm
import face_recognition
import numpy as np


class UniqueFaceDetector(FacesDetectorInterface):
    known_encodings: List[np.array] = []

    def detect(
        self,
        frames: List[RetrievedFrameResponse],
        number_of_upsamples: int = 0,
        locate_model: str = "fog",
        num_jitters: int = 1,
        encode_model: str = "small",
        tolerance: float = 0.6,
    ) -> List[DetectedFaceResponse]:
        self.known_encodings = []

        detected_faces: List[DetectedFaceResponse] = []
        for i, frame in enumerate(tqdm(frames, "Faces detection")):
            assert isinstance(frame, RetrievedFrameResponse)
            image = np.array(frame.img)
            locations = face_recognition.face_locations(image, number_of_upsamples, locate_model)
            encodings = face_recognition.face_encodings(image, locations, num_jitters, encode_model)

            j = 0
            for (top, right, bottom, left), encoding in zip(locations, encodings):
                if self.is_known(encoding, tolerance):
                    # Face already is found and should be skipped
                    continue

                # Crop the face from frame and add to results
                face = frame.img.crop(box=(left, top, right, bottom))
                box = self.create_box(left, top, right, bottom)
                detected_faces.append(DetectedFaceResponse(f"face-{i}-{j}", face, frame.ts, frame.pts, box, encoding))
                j += 1

            # @TODO Add frame saving if it is required

        return detected_faces

    def is_known(self, encoding: np.array, tolerance: float) -> bool:
        results = face_recognition.compare_faces(self.known_encodings, encoding, tolerance)
        if True in results:
            return True

        self.known_encodings.append(encoding)
        return False

    def create_box(self, left, top, right, bottom) -> dict:
        return {"left": left, "top": top, "right": right, "bottom": bottom}
