from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.audit import Audit
from app.services.domaine_service import create_empty_domaine
import app.globals as globals

def get_all_audits(db: Session):
    return db.query(Audit).all()

def get_audit_by_id(audit_id: int, db: Session):
    return db.query(Audit).filter(Audit.id_audit == audit_id).first()

def create_new_audit(url_domaine : str, db: Session):
    if globals.CONNECTED_USER is not None:
        id_domaine = create_empty_domaine(url_domaine, db)
        new_audit = Audit(
            date=datetime.now(),
            etat=0, 
            path_rapport="",
            id_user=globals.CONNECTED_USER.id_user, 
            id_domaine=id_domaine
        )
        
        db.add(new_audit)
        db.commit()
        db.refresh(new_audit)
        
        globals.CURRENT_AUDIT = new_audit

        return True
    else:
        raise HTTPException(status_code=500, detail=f"Utilisateur non connecté")
        