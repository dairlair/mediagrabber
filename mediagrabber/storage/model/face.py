from sqlalchemy import Column, BigInteger, String, Float, SmallInteger, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql.expression import text
from mediagrabber.storage.model.base import Base


class Face(Base):
    __tablename__ = "faces"

    id = Column(BigInteger, primary_key=True)
    urlId = Column("url_id", BigInteger, nullable=False)
    ts = Column(Float, nullable=False)
    box = Column(ARRAY(SmallInteger, as_tuple=True))  # Face paddings, in the CSS format (top, right, bottom, left)
    entity = Column(String, nullable=False, default="")
    entityId = Column("entity_id", String, nullable=False, default=0)
    tags = Column(ARRAY(String), nullable=False, default=[])
    encoder = Column(String, nullable=False)
    encoding = Column(ARRAY(Float), nullable=False)
    createdAt = Column("created_at", DateTime(timezone=True), nullable=False, default=text("CURRENT_TIMESTAMP"))

    def __repr__(self):
        return f"<Face(id={self.id}, urlId={self.urlId}, ts={self.ts}, box={self.box})"
