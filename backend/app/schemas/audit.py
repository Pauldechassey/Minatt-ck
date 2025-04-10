from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AuditSchema(BaseModel):
    id_audit: int
    date: datetime
    etat: int
    path_rapport: Optional[str]
    id_user: int
    id_domaine: int

    class Config:
        orm_mode = True

class UrlRequest(BaseModel):
    url_domaine: str