from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from db.database import Base
from sqlalchemy.orm import relationship

class Media(Base):

    __tablename__ = "medias"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    chemin = Column(String, nullable=False)
    type = Column(String, nullable=False)
    mime_type = Column(String, nullable=False)
    taille = Column(Integer, nullable=False)
    dateCreation = Column(Date, nullable=False)
    dateMaj = Column(Date, nullable=False)


    assos = relationship(
        "MediaAsso",
        back_populates="media"
    )