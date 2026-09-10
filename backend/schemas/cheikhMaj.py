from pydantic import BaseModel, Field, StringConstraints
from datetime import date
from typing import Annotated

# Define a reusable long text type
LongText = Annotated[str, StringConstraints(max_length=10000)]

class CheikhMaj(BaseModel):
    nom : str = Field(min_length=3)
    prenom : str = Field(min_length=3)
    bio : LongText
    foyer : str = Field(min_length=4)
    dateMaj : date = date.today()
