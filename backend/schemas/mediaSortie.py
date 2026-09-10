from datetime import date
from pydantic import BaseModel


class MediaSortie(BaseModel):
    id: int
    nom: str
    chemin: str
    type: str
    mime_type: str
    taille: int
    dateCreation: date
    dateMaj: date

    class Config:
        from_attributes = True