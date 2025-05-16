from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response, JSONResponse
from sqlalchemy.orm import Session
from pathlib import Path
import shutil
import os
from minattack.backend.app.database.database import SessionLocal
from minattack.backend.app.services.rapport_service import rapport, path_file

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/rapport", tags=["Rapport"])

@router.get("/{id_audit}")
def read_rapport(id_audit: int, db: Session = Depends(get_db)):
    """Retourne le rapport PDF directement au navigateur"""
    try:
        # Générer le contenu du rapport
        rapport_pdf = rapport(id_audit, db)
        
        filename = path_file(id_audit, db)
        return Response(
            content=rapport_pdf,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'inline; filename="{filename}"' #inline -> s'ouvre dans un navigateur
            }
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur lors de la génération du rapport: {str(e)}"
        )


@router.get("/download/{id_audit}")
def download_rapport(id_audit: int, db: Session = Depends(get_db)):
    """Télécharge le rapport PDF"""
    try:
        # Générer le contenu du rapport
        rapport_pdf = rapport(id_audit, db)
        
        filename = path_file(id_audit, db)
        
        return Response(
            content=rapport_pdf,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"' #attachment -> se télécharge
            }
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur lors de la génération du rapport: {str(e)}"
        )