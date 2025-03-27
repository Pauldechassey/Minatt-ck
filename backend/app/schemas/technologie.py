from pydantic import BaseModel


class TechnologieSchema(BaseModel):
    id_techno: int
    nom_techno: str
    version_techno: str

    class Config:
        orm_mode = True