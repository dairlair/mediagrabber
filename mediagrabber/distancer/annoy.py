import logging
from mediagrabber.core import StorageInterface, DistancerInterface
from annoy import AnnoyIndex

class AnnoyDistancer(DistancerInterface):
    def get_nns_by_face_id(self, face_id, n, search_k=-1, include_distances=False):
        # Build index
        t = AnnoyIndex(128, 'euclidean')
        for faces in self.storage.get_faces():
            t.add_item(faces['id'], faces['encoding'])
        logging.info('Build index...')
        t.build(10)  # 10 trees
        # Find nearest neighbors
        return t.get_nns_by_item(face_id, n, -1, include_distances)

