from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from db.database import Base
from sqlalchemy.orm import relationship

class Wadjou(Base):
    __tablename__ = "wadjous"

    id = Column(Integer, primary_key=True, index=True)
    libelle = Column(String)
    medialink = Column(Text)
    dateCreation = Column(Date)
    dateMaj = Column(Date)
    id_cheikh = Column(Integer, ForeignKey("cheikhs.id"))

    #cheikh = relationship("Cheikh", back_populates="wadjous")
