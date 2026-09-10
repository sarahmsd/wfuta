from pydantic import BaseModel, Field, StringConstraints
from datetime import date
from typing import Annotated

# Define a reusable long text type
LongText = Annotated[str, StringConstraints(max_length=10000)]

class ArticleCreation(BaseModel):
    titre : str = Field(min_length=3)
    excert : str = Field(min_length=1)
    content : LongText
    dateCreation : date = date.today()
    dateMaj : date = date.today()

