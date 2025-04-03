from pydantic import BaseModel

class SousDomaineSchema(BaseModel):
    id_SD: int
    url_SD: str
    description_SD: str
    id_domaine: int

    class Config:
        from_attributes = True