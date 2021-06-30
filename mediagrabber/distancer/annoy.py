import logging
from mediagrabber.storage.model.face import Face
from typing import List
from mediagrabber.core import FaceDistance, DistancerInterface, StorageInterface
from annoy import AnnoyIndex


class AnnoyDistancer(DistancerInterface):
    def __init__(self, storage: StorageInterface, dimensions: int = 128) -> None:
        super().__init__(storage)
        self.dimensions = dimensions

    def get_nns_by_face_id(self, faceId: int, n: int, tags: List[str]) -> List[FaceDistance]:
        # Build index
        t = AnnoyIndex(self.dimensions, "euclidean")
        for face in self.storage.get_faces(tags):
            t.add_item(face.id, face.encoding)
        logging.info("Build index...")
        t.build(10)  # 10 trees
        # The recognized faceId may be not in the faces with specified tags, we need retrieve it
        face: Face = self.storage.get_face_by_id(faceId)
        if face is None:
            return None

        # Find nearest neighbors
        distances: List[FaceDistance] = []
        nns = t.get_nns_by_vector(face.encoding, n, search_k=-1, include_distances=True)
        if len(nns) > 0:
            for dis in zip(nns[0], nns[1]):
                distances.append(FaceDistance(dis[0], dis[1]))

        return distances
