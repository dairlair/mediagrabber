from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, BigInteger, String

Base = declarative_base()


class Url(Base):
    __tablename__ = "urls"

    id = Column(BigInteger, primary_key=True)
    url = Column(String, unique=True)

    def __repr__(self):
        return f"<URL(id={self.id}, url='{self.url}')"
