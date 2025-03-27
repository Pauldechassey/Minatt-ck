from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.sous_domaine import SousDomaineSchema
from app.services.sous_domaine_service import get_all_sous_domaines, get_sous_domaine_by_id, get_sous_domaines_by_domaine
from app.database import SessionLocal

router = APIRouter(prefix="/sous-domaines", tags=["Sous-Domaines"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[SousDomaineSchema])
def read_sous_domaines(db: Session = Depends(get_db)):
    return get_all_sous_domaines(db)

@router.get("/{sous_domaine_id}", response_model=SousDomaineSchema)
def read_sous_domaine(sous_domaine_id: int, db: Session = Depends(get_db)):
    sous_domaine = get_sous_domaine_by_id(sous_domaine_id, db)
    if not sous_domaine:
        raise HTTPException(status_code=404, detail="Sous-domaine not found")
    return sous_domaine

@router.get("/domaine/{domaine_id}", response_model=list[SousDomaineSchema])
def read_sous_domaines_by_domaine(domaine_id: int, db: Session = Depends(get_db)):
    return get_sous_domaines_by_domaine(domaine_id, db)