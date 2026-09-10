from datetime import date
from pydantic import BaseModel


class MediaForEntitySortie(BaseModel):
    id: int
    nom: str
    chemin: str
    type: str
    mime_type: str
    taille: int
    dateCreation: date
    dateMaj: date
    role: str | None = None
    url: str