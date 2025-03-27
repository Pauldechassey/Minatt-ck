from pydantic import BaseModel


class TypeAttaqueSchema(BaseModel):
    id_Type: int
    nom_type: str
    description_type: str

    class Config:
        orm_mode = True