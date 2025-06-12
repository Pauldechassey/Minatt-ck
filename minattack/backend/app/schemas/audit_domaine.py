from pydantic import BaseModel
from datetime import datetime


class AuditDomaineSchema(BaseModel):
    id_audit: int
    date: datetime
    url_domaine: str
    etat: int

    class Config:
        from_attributes = True
