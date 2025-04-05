from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict
from backend.app.models.sous_domaine import SousDomaine 
from backend.app.database import SessionLocal
from backend.app.services.attaque_service import run_attacks
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
@router.post("/list/", summary="Lister les attaques. ex : [sqli, xss]", status_code=200)
def attaque_sqli(SD_initial_id: int, db: Session = Depends(get_db), attaque_type: List[str] = Query(...)):
    if run_attacks(SD_initial_id, attaque_type, db):
        return {"message": "Attaque SQLi effectuée avec succès"}
    else:
        raise HTTPException(status_code=404, detail="Sous-domaine non trouvé")

##
@router.post("/sqli/", summary="Attaque SQLi", status_code=200)
def attaque_sqli(SD_initial_id: int, db: Session = Depends(get_db)):
    if run_attacks(SD_initial_id, ["sqli"], db):
        return {"message": "Attaque SQLi effectuée avec succès"}
    else:
        raise HTTPException(status_code=404, detail="Sous-domaine non trouvé")

##
@router.post("/xss/", summary="Attaque XSS", status_code=200)
def attaque_xss(SD_initial_id: int, db: Session = Depends(get_db)):
    if run_attacks(SD_initial_id, ["xss"], db):
        return {"message": "Attaque XSS effectuée avec succès"}
    else:
        raise HTTPException(status_code=404, detail="Sous-domaine non trouvé")

##
@router.post("/csrf/", summary="Attaque CSRF", status_code=200)
def attaque_csrf(SD_initial_id: int, db: Session = Depends(get_db)):
    if run_attacks(SD_initial_id, ["csrf"], db):
        return {"message": "Attaque CSRF effectuée avec succès"}
    else:
        raise HTTPException(status_code=404, detail="Sous-domaine non trouvé")

##
@router.post("/headers_cookies/", summary="Attaque Header_Cookie", status_code=200)
def attaque_headers_cookies(SD_initial_id: int, db: Session = Depends(get_db)):
    if run_attacks(SD_initial_id, ["headers_cookies"], db):
        return {"message": "Attaque Header/Cookie effectuée avec succès"}
    else:
        raise HTTPException(status_code=404, detail="Sous-domaine non trouvé")