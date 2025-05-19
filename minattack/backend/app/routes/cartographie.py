from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from minattack.backend.app.database.database import SessionLocal
from minattack.backend.app.scripts.cartographie_script import run_cartographie
from minattack.backend.app.models.audit import Audit
from minattack.backend.app.models.domaine import Domaine

router = APIRouter()
logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/cartographie", tags=["Cartographie"])

@router.post("/{audit_id}", summary="Cartographie à partir d'un audit", status_code=200)
def cartographie_from_audit(audit_id: int, db: Session = Depends(get_db)):
    """
    Exécute une cartographie BFS en partant du domaine associé à un audit spécifique.
    
    Args:
        audit_id (int): ID de l'audit pour lequel effectuer la cartographie
        db (Session): Session de base de données
        
    Returns:
        dict: Message de succès ou erreur
    """
    audit = db.query(Audit).filter(Audit.id_audit == audit_id).first()
    
    if not audit:
        raise HTTPException(status_code=404, detail=f"Audit avec ID {audit_id} non trouvé")
    
    domaine = db.query(Domaine).filter(Domaine.id_domaine == audit.id_domaine).first()
    
    if not domaine:
        raise HTTPException(status_code=404, detail=f"Aucun domaine trouvé pour l'audit {audit_id}")
    
    # Exécuter la cartographie BFS à partir du domaine de l'audit
    if run_cartographie(domaine.url_domaine, db, id_audit=audit_id, id_domaine=domaine.id_domaine):
        db.commit()
        return {
            "message": f"Cartographie BFS effectuée avec succès pour l'audit {audit_id}",
            "domaine": domaine.url_domaine,
            "id_domaine": domaine.id_domaine
        }
    else:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Échec de la cartographie pour l'audit {audit_id} sur le domaine {domaine.url_domaine}"
        )