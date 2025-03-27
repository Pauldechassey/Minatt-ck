from pydantic import BaseModel

class SousDomaineSchema(BaseModel):
    id_SD: int
    url_SD: str | None = None
    description_SD: str | None = None
    id_domaine: int

    class Config:
        from_attributes = True