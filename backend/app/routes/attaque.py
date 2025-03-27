from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from backend.app.database.database import SessionLocal
from backend.app.services.attaque_service import run_attack_on_urls
from backend.app.services.sous_domaine_service import get_all_child_urls_recursively
from sqlalchemy.orm import Session


router = APIRouter(prefix="/attaque", tags=["Attaque"])

# probleme dans les routes: on appelle plusieurs fois la focntion urls_cibles = get_all_child_urls_recursively(url)
# si on veut lancer plusieurs attaques en meme temps

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

##
@router.post("/all/{url}", response_model=List[Dict])
def attaque_sqli(url: str, db: Session = Depends(get_db)):
    urls_cibles = get_all_child_urls_recursively(url)
    if not urls_cibles:
        raise HTTPException(status_code=404, detail="Aucune URL trouvée pour cette attaque.")
    resultats = run_attack_on_urls(urls_cibles, "all")
    
    return {"url_cible": url, "resultats": resultats}

##
@router.post("/sqli/{url}", response_model=List[Dict])
def attaque_sqli(url: str, db: Session = Depends(get_db)):
    urls_cibles = get_all_child_urls_recursively(url)
    if not urls_cibles:
        raise HTTPException(status_code=404, detail="Aucune URL trouvée pour cette attaque.")
    resultats = run_attack_on_urls(urls_cibles, "sqli")
    
    return {"url_cible": url, "resultats": resultats}

##
@router.post("/xss/{url}", response_model=List[Dict])
def attaque_sqli(url: str, db: Session = Depends(get_db)):
    urls_cibles = get_all_child_urls_recursively(url)
    if not urls_cibles:
        raise HTTPException(status_code=404, detail="Aucune URL trouvée pour cette attaque.")
    resultats = run_attack_on_urls(urls_cibles, "xss")
    
    return {"url_cible": url, "resultats": resultats}

##
@router.post("/csrf/{url}", response_model=List[Dict])
def attaque_sqli(url: str, db: Session = Depends(get_db)):
    urls_cibles = get_all_child_urls_recursively(url)
    if not urls_cibles:
        raise HTTPException(status_code=404, detail="Aucune URL trouvée pour cette attaque.")
    resultats = run_attack_on_urls(urls_cibles, "csrf")
    
    return {"url_cible": url, "resultats": resultats}

##
@router.post("/headers_cookies/{url}", response_model=List[Dict])
def attaque_sqli(url: str, db: Session = Depends(get_db)):
    urls_cibles = get_all_child_urls_recursively(url)
    if not urls_cibles:
        raise HTTPException(status_code=404, detail="Aucune URL trouvée pour cette attaque.")
    resultats = run_attack_on_urls(urls_cibles, "headers_cookies")
    
    return {"url_cible": url, "resultats": resultats}
