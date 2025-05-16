
from fastapi import APIRouter

from minattack.backend.app.database.database import SessionLocal


router = APIRouter(prefix="/rapport", tags=["Rapport"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/:id_audit")
def read_rapport():
    return {"message": "endpoint pour récupérer le rapport d'un audit spécifique"}

