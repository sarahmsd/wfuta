from pydantic import BaseModel, Field, StringConstraints
from datetime import date
from typing import Annotated

# Define a reusable long text type
LongText = Annotated[str, StringConstraints(max_length=10000)]

class WadjouMaj(BaseModel):
    libelle : str
    medialink : str
    dateMaj : date = date.today()