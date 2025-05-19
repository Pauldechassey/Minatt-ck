from pydantic import BaseModel


class SousDomaineSchema(BaseModel):
    id_SD: int
    url_SD: str
    description_SD: str
    degre: int
    id_domaine: int
    id_SD_Sous_domaine: int

    class Config:
        from_attributes = True
