from fastapi import APIRouter, Depends, HTTPException
from minattack.backend.app.database import SessionLocal
from minattack.backend.app.schemas.type_attaque import TypeAttaqueResquest
from minattack.backend.app.services.attaque_service import run_attacks
from sqlalchemy.orm import Session

router = APIRouter(prefix="/attaque", tags=["Attaque"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

##
@router.post("/all/", summary="Attaque ALL", status_code=200)
def attaque_all(SD_initial_id: int, db: Session = Depends(get_db)):
    if run_attacks(SD_initial_id, ["all"], db):
        return {"message": "Attaque ALL effectuée avec succès"}
    else:
        raise HTTPException(status_code=404, detail="Sous-domaine non trouvé")

##
@router.post("/recursive/list/", summary="Lister les attaques. ex : [sqli, xss] pour les enfants", status_code=200)
def attaque_sqli(SD_initial_id: int, type : TypeAttaqueResquest, db: Session = Depends(get_db)):
    if run_attacks(SD_initial_id, type.attaque_type, db): #single = false
        return {"message": "Attaque SQLi effectuée avec succès"}
    else:
        raise HTTPException(status_code=404, detail="Sous-domaine non trouvé")

##
@router.post("/single/list/", summary="Lister les attaques. ex : [sqli, xss] pour UNE url", status_code=200)
def attaque_sqli(SD_initial_id: int, type : TypeAttaqueResquest, db: Session = Depends(get_db)):
    if run_attacks(SD_initial_id, type.attaque_type, db, True): #single = true
        return {"message": "Attaque SQLi effectuée avec succès"}
    else:
        raise HTTPException(status_code=404, detail="Sous-domaine non trouvé")