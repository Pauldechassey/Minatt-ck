from typing import List
from pydantic import BaseModel


class TypeAttaqueSchema(BaseModel):
    id_Type: int
    nom_type: str
    description_type: str

    class Config:
        from_attributes = True


class TypeAttaqueResquest(BaseModel):
    attaque_type: List[str]
