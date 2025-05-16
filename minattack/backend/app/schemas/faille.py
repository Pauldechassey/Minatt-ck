from pydantic import BaseModel


class FailleSchema(BaseModel):
    id_faille: int
    gravite: int
    Description: str
    balise: str
    id_attaque: int

    class Config:
        orm_mode = True
