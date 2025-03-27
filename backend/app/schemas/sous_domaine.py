from pydantic import BaseModel, HttpUrl
from typing import Optional


class SousDomaineBase(BaseModel):
    id_SD: int
    url_SD: HttpUrl

class SousDomaineCreate(SousDomaineBase):
    id_domaine: int

class SousDomaineSchema(BaseModel):
    id_SD: int
    url_SD: HttpUrl
    description_SD: str
    degre: int
    id_domaine: int
    id_SD_Sous_domaine: Optional[int]

    class Config:
        orm_mode = True