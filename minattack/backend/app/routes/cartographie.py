from fastapi import APIRouter, Depends, HTTPException
from minattack.backend.app.database import SessionLocal
from sqlalchemy.orm import Session
import logging

from minattack.backend.app.services.audit_service import get_audit_by_id
from minattack.backend.app.services.cartographie_service import run_cartographie

router = APIRouter(prefix="/cartographie", tags=["Cartographie"])
logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/all/", summary="Cartographie ALL", status_code=200)
def cartographie_all(id_audit: int, db: Session = Depends(get_db)):
    audit = get_audit_by_id(id_audit, db)
    if not audit:
        raise HTTPException(status_code=404, detail=f"Audit avec ID {id_audit} non trouvé")
    
    try:
        logger.info(f"Démarrage cartographie pour domaine ID: {audit.id_domaine}")
        nb_sd = run_cartographie(audit, db)
        if nb_sd > 0:
            return {"message": f"Cartographie effectuée avec succès : {nb_sd} sous-domaines trouvés"}
        else:
            raise HTTPException(status_code=404, detail="Aucun sous-domaine trouvé")
    except Exception as e:
        logger.error(f"Erreur lors de la cartographie: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))