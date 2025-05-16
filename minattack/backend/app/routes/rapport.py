from fastapi import APIRouter, Depends, HTTPException
from pathlib import Path
from sqlalchemy.orm import Session
import shutil
import os

from minattack.backend.app.database.database import SessionLocal
from minattack.backend.app.services.rapport_service import path_file, rapport
from minattack.backend.app.scripts.rapport_script import get_rapport_dir


router = APIRouter(prefix="/rapport", tags=["Rapport"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{id_audit}")
def read_rapport(id_audit: int, db: Session = Depends(get_db)):
    rapport_pdf = rapport(id_audit, db)
    return rapport_pdf


@router.get("/download/{id_audit}")
def download_rapport(id_audit: int, db: Session = Depends(get_db)):
    """Copie le rapport PDF dans le dossier Downloads de l'utilisateur"""
    try:
        filename = path_file(id_audit, db)
        
        source_file = get_rapport_dir() / filename
        
        downloads_path = Path.home() / "Downloads"
        dest_file = downloads_path / filename

        if not source_file.exists():
            raise HTTPException(
                status_code=404,
                detail="Le rapport PDF n'a pas été trouvé"
            )
            
        # Copier le fichier
        shutil.copy2(source_file, dest_file)
        
        return {
            "status": "success",
            "message": f"Rapport copié dans {dest_file}",
            "file_path": str(dest_file)
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la copie du rapport: {str(e)}"
        )
