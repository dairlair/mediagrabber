import logging
from typing import List
from mediagrabber.core import FaceDistance, DistancerInterface
from annoy import AnnoyIndex


class AnnoyDistancer(DistancerInterface):
    def get_nns_by_face_id(self, faceId: int, n: int, tags: List[str]):
        # Build index
        t = AnnoyIndex(128, "euclidean")
        for face in self.storage.get_faces(tags):
            t.add_item(face.id, face.encoding)
        logging.info("Build index...")
        t.build(10)  # 10 trees
        # Find nearest neighbors
        distances: List[FaceDistance] = []
        nns = t.get_nns_by_item(faceId, n, search_k=-1, include_distances=True)
        if len(nns) > 0:
            for dis in zip(nns[0], nns[1]):
                distances.append(FaceDistance(dis[0], dis[1]))

        return distances
