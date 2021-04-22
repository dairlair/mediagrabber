import numpy as np
from typing import List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mediagrabber.storage.model.url import Url
from mediagrabber.storage.model.face import Face


class PostgreSQLStorage:
    def __init__(self, dsn: str):
        engine = create_engine(dsn, echo=True, future=True)
        self.session = sessionmaker(engine)

    def get_url_id_or_create(self, url: str) -> int:
        id = self.get_url_id(url)
        if id:
            return id

        with self.session() as session:
            model = Url(url=url)
            session.add(model)
            session.commit()
            return model.id

    def get_url_id(self, url: str) -> Optional[int]:
        with self.session() as session:
            model = session.query(Url).filter_by(url=url).first()
            return model.id if model else None

    def get_faces(self, tags: List[str]) -> List[dict]:
        # try:
        #     cur = self.get_connection().cursor()
        #     if len(tags) > 0:
        #         cur.execute("SELECT id, encoding FROM faces WHERE tags = ANY(%s)", (tags, 1))
        #     else:
        #         cur.execute("SELECT id, encoding FROM face")
        #     rows = cur.fetchall()
        #     return rows
        # finally:
        #     cur.close()
        raise NotImplementedError

    def save_encoding(
        self,
        urlId: int,
        ts: float,
        faceId: int,
        box: List[int],
        entity: str,
        entityId: int,
        tags: List[str],
        encoder: str,
        encoding: np.array,
    ) -> int:
        with self.session() as session:
            model: Face = Face()
            model.urlId = urlId
            model.ts = ts
            model.faceId = faceId
            model.box = box
            model.entity = entity
            model.entityId = entityId
            model.tags = tags
            model.encoder = encoder
            model.encoding = encoding
            session.add(model)
            session.commit()
            return model.id
