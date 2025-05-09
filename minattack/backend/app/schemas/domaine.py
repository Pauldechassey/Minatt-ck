from pydantic import BaseModel
from typing import Optional


class DomaineSchema(BaseModel):
    id_domaine: int
    url_domaine: str
    description_domaine: Optional[str]

    class Config:
        orm_mode = True