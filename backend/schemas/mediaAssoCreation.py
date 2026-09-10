from pydantic import BaseModel
from typing import Optional


class MediaAssoCreation(BaseModel):
    entity_type: str
    entity_id: int
    role: Optional[str] = None