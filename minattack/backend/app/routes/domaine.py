from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from minattack.backend.app.schemas.domaine import DomaineSchema
from minattack.backend.app.services.domaine_service import (
    get_all_domaines,
    get_domaine_by_id,
)
from minattack.backend.app.database import SessionLocal

router = APIRouter(prefix="/domaines", tags=["Domaines"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[DomaineSchema])
def read_domaines(db: Session = Depends(get_db)):
    return get_all_domaines(db)


@router.get("/{domaine_id}", response_model=DomaineSchema)
def read_domaine(domaine_id: int, db: Session = Depends(get_db)):
    domaine = get_domaine_by_id(domaine_id, db)
    if not domaine:
        raise HTTPException(status_code=404, detail="Domaine not found")
    return domaine
