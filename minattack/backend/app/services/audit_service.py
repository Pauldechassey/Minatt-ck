from datetime import datetime
from typing import cast
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from minattack.backend.app.models.audit import Audit
from minattack.backend.app.models.domaine import Domaine
from minattack.backend.app.services.domaine_service import create_empty_domaine
import minattack.backend.app.globals as globals


def get_all_audits(db: Session):
    if globals.CONNECTED_USER is not None:
        return db.query(Audit).all()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Utilisateur non connecté",
        )


def get_audits_and_domaines(db: Session):
    results = (
        db.query(Audit.id_audit, Audit.date, Audit.etat, Domaine.url_domaine)
        .join(Domaine, Audit.id_domaine == Domaine.id_domaine)
        .all()
    )
    return [
        {
            "id_audit": row.id_audit,
            "date": row.date,
            "url_domaine": row.url_domaine,
            "etat": row.etat,
        }
        for row in results
    ]


def get_audit_by_id(audit_id: int, db: Session):
    if globals.CONNECTED_USER is not None:
        return db.query(Audit).filter(Audit.id_audit == audit_id).first()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Utilisateur non connecté",
        )


def create_new_audit(url_domaine: str, db: Session):
    if globals.CONNECTED_USER is not None:
        id_domaine = create_empty_domaine(url_domaine, db)
        new_audit = Audit(
            date=datetime.now(),
            etat=0,
            path_rapport="",
            id_user=globals.CONNECTED_USER.id_user,
            id_domaine=id_domaine,
        )
        db.add(new_audit)
        db.commit()
        db.refresh(new_audit)
        globals.CURRENT_AUDIT = new_audit
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Utilisateur non connecté",
        )


def update_audit_state(audit_id: int, new_state: int, db: Session):
    if globals.CONNECTED_USER is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur non connecté",
        )
    audit = db.query(Audit).filter(Audit.id_audit == audit_id).first()
    if audit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Audit non trouvé"
        )
    try:
        audit.etat = new_state
        db.commit()
        db.refresh(audit)
        print("----------------")
        print(audit.etat)
        print("----------------")
        globals.CURRENT_AUDIT = audit
        return True
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la mise à jour de l'état : {str(e)}",
        )
