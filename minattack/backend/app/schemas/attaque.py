from pydantic import BaseModel
from datetime import datetime


class AttaqueSchema(BaseModel):
    id_attaque: int
    payload: str
    date_attaque: datetime
    resultat: int
    id_SD: int
    id_Type: int

    class Config:
        orm_mode = True
