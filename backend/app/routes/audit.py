from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.app.schemas.audit import AuditSchema, UrlRequest
from backend.app.services.audit_service import create_new_audit, get_all_audits, get_audit_by_id
from backend.app.database import SessionLocal

router = APIRouter(prefix="/audits", tags=["Audits"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/all", response_model=list[AuditSchema])
def read_audits(db: Session = Depends(get_db)):
    return get_all_audits(db)

@router.get("/{audit_id}", response_model=AuditSchema)
def read_audit(audit_id: int, db: Session = Depends(get_db)):
    audit = get_audit_by_id(audit_id, db)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    return audit

@router.post("/new", status_code=201)
def new_audit(url : UrlRequest, db: Session = Depends(get_db)):
    try:
        if create_new_audit(url.url_domaine, db):
            return {"message": "Audit créé avec succès"}  
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création de l'audit: {str(e)}")
