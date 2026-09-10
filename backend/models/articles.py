from sqlalchemy import Column, Integer, String, Date, Text
from db.database import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String)
    excert = Column(String)
    content = Column(Text)
    dateCreation = Column(Date)
    dateMaj = Column(Date)
