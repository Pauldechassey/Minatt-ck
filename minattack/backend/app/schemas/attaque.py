from pydantic import BaseModel
from datetime import datetime
from typing import List


class AttaqueSchema(BaseModel):
    id_attaque: int
    payload: str
    date_attaque: datetime
    resultat: int
    id_SD: int
    id_Type: int

    class Config:
        from_attributes = True

class AttackRequest(BaseModel):
    SD_initial_id: int
    attaque_type: List[str]
