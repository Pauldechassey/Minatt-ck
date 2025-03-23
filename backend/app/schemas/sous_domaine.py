from pydantic import BaseModel
from typing import Optional

class SousDomaineSchema(BaseModel):
    id_SD: int
    url_SD: str
    description_SD: str
    degre: int
    id_domaine: int
    id_SD_Sous_domaine: Optional[int]

    class Config:
        orm_mode = True