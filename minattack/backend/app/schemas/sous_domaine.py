from pydantic import BaseModel
from typing import Optional


class SousDomaineSchema(BaseModel):
    id_SD: int
    url_SD: str
    description_SD: Optional[str] = None
    degre: int
    id_domaine: int
    id_SD_Sous_domaine: Optional[int] = None  # Permettre None ici

    class Config:
        from_attributes = True
