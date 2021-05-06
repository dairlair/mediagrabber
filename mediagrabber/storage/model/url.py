from sqlalchemy import Column, BigInteger, String
from mediagrabber.storage.model.base import Base


class Url(Base):
    __tablename__ = "urls"

    id = Column(BigInteger, primary_key=True)
    url = Column(String, unique=True)

    def __repr__(self):
        return f"<Url(id={self.id}, url='{self.url}')"
