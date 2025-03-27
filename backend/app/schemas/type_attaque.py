from pydantic import BaseModel
from  app.schemas.type_attaque_enum import TypeAttaque

class TypeAttaqueSchema(BaseModel):
    id_Type: int
    nom_type: TypeAttaque
    description_type: str

    class Config:
        orm_mode = True