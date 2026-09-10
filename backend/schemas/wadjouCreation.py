from pydantic import BaseModel, Field, StringConstraints
from datetime import date
from typing import Annotated

# Define a reusable long text type
LongText = Annotated[str, StringConstraints(max_length=10000)]

class WadjouCreation(BaseModel):
    libelle : str
    medialink : str
    dateCreation : date = date.today()
    dateMaj : date = date.today()
    id_cheikh : int