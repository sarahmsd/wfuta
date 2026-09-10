from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base


class MediaAsso(Base):
    __tablename__ = "media_asso"

    id = Column(Integer, primary_key=True, index=True)

    media_id = Column(Integer, ForeignKey("medias.id"), nullable=False)

    entity_type = Column(String, nullable=False)

    entity_id = Column(Integer, nullable=False)

    role = Column(String, nullable=True)

    media = relationship("Media", back_populates="assos")