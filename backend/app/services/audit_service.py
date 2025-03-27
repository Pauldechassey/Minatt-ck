from sqlalchemy.orm import Session
from app.models.audit import Audit

def get_all_audits(db: Session):
    return db.query(Audit).all()

def get_audit_by_id(audit_id: int, db: Session):
    return db.query(Audit).filter(Audit.id_audit == audit_id).first()
