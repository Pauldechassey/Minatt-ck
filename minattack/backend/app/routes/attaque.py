from fastapi import APIRouter, Depends, HTTPException
from minattack.backend.app.database import SessionLocal
from minattack.backend.app.globals import CURRENT_AUDIT
from minattack.backend.app.schemas.type_attaque import TypeAttaqueResquest
from minattack.backend.app.services.attaque_service import run_attacks, run_cluster_attacks
from sqlalchemy.orm import Session


router = APIRouter(prefix="/attaque", tags=["Attaque"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/list/cluster", summary="Attaque sur les centres de clusters : Lister les attaques '[sqli, xss, ...]'  et fournir l'id de l'audit en question", status_code=200)  
def attaque_all_cluster(SD_initial_id: int, type: TypeAttaqueResquest,   db: Session = Depends(get_db)):
    if run_cluster_attacks(SD_initial_id, type.attaque_type, db):
        return {"message": "Attaque ALL sur les centres de clusters effectuée avec succès"}  
    else:
        raise HTTPException(status_code=404, detail="Audit non trouvé ou pas de sous-domaines associés")


##
@router.post(
    "/list/",
    summary="Lister les attaques. ex : [sqli, xss] pour les enfants",
    status_code=200,
)
def attaque(
    id_audit: int, type: TypeAttaqueResquest, db: Session = Depends(get_db)
):
    
    if run_attacks(id_audit, type.attaque_type, db):  # single = false
        return {"message": "Attaques effectuées avec succès"}
    else:
        raise HTTPException(status_code=404, detail="Sous-domaine non trouvé")
