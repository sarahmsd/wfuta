from sqlalchemy import Column, Integer, String, Date, Text
from db.database import Base
from sqlalchemy.orm import relationship

class Cheikh(Base):
    __tablename__ = "cheikhs"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    prenom = Column(String)
    bio = Column(Text)
    foyer = Column(Text)
    dateCreation = Column(Date)
    dateMaj = Column(Date)

    #wadjous = relationship("Wadjou", back_populates="cheikh")