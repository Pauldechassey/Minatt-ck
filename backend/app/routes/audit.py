from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.schemas.audit import AuditSchema
from backend.app.services.audit_service import get_all_audits, get_audit_by_id
from backend.app.database import SessionLocal

router = APIRouter(prefix="/audits", tags=["Audits"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[AuditSchema])
def read_audits(db: Session = Depends(get_db)):
    return get_all_audits(db)

@router.get("/{audit_id}", response_model=AuditSchema)
def read_audit(audit_id: int, db: Session = Depends(get_db)):
    audit = get_audit_by_id(audit_id, db)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    return audit
