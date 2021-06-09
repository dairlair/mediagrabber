import numpy as np
from typing import List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mediagrabber.storage.model.url import Url
from mediagrabber.storage.model.face import Face


class PostgreSQLStorage:
    def __init__(self, dsn: str):
        engine = create_engine(dsn, future=True)
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

    def get_faces(self, tags: List[str]) -> List[Face]:
        with self.session() as session:
            if len(tags):
                return session.query(Face).filter(Face.tags.overlap([tags])).all()
            else:
                return session.query(Face).all()

    def save_encoding(
        self,
        urlId: int,
        ts: float,
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
            model.box = box
            model.entity = entity
            model.entityId = entityId
            model.tags = tags
            model.encoder = encoder
            model.encoding = encoding
            session.add(model)
            session.commit()
            return model.id
