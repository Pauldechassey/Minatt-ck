from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict
from app.database.database import SessionLocal
from app.services.attaque_service import run_attack_on_urls
from app.services.sous_domaine_service import get_all_child_urls_recursively
from sqlalchemy.orm import Session

router = APIRouter(prefix="/attaque", tags=["Attaque"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

##
def lancer_attaque(url: str, attaque_type: str):
    urls_cibles = get_all_child_urls_recursively(url)
    if not urls_cibles:
        raise HTTPException(status_code=404, detail="Aucune URL trouvée pour cette attaque.")
    resultats = run_attack_on_urls(urls_cibles, attaque_type)
    return {"url_cible": url, "resultats": resultats}

##
@router.post("/all/", response_model=Dict, summary="Attaque ALL")
def attaque_all(url: str = Query(..., description="URL cible"), db: Session = Depends(get_db)):
    return lancer_attaque(url, "all")

##
@router.post("/sqli/", response_model=Dict, summary="Attaque SQLi")
def attaque_sqli(url: str = Query(..., description="URL cible"), db: Session = Depends(get_db)):
    return lancer_attaque(url, "sqli")

##
@router.post("/xss/", response_model=Dict, summary="Attaque XSS")
def attaque_xss(url: str = Query(..., description="URL cible"), db: Session = Depends(get_db)):
    return lancer_attaque(url, "xss")

##
@router.post("/csrf/", response_model=Dict, summary="Attaque CSRF")
def attaque_csrf(url: str = Query(..., description="URL cible"), db: Session = Depends(get_db)):
    return lancer_attaque(url, "csrf")

##
@router.post("/headers_cookies/", response_model=Dict, summary="Attaque Header_Cookie")
def attaque_headers_cookies(url: str = Query(..., description="URL cible"), db: Session = Depends(get_db)):
    return lancer_attaque(url, "headers_cookies")
