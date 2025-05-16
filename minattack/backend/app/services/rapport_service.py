from fastapi import HTTPException
import logging
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from minattack.backend.app.models.audit import Audit
from minattack.backend.app.models.sous_domaine import SousDomaine
from minattack.backend.app.models.domaine import Domaine
from minattack.backend.app.models.attaque import Attaque
from minattack.backend.app.models.type_attaque import Type_attaque
from minattack.backend.app.models.faille import Faille

from typing import Dict, List
from datetime import datetime
from io import BytesIO
from minattack.backend.app.scripts.rapport_script import generer_rapport

def get_audit_data(db: Session, audit_id: int) -> Dict:
    """Récupère toutes les données nécessaires pour le rapport"""

    # Vérification/récupération audit et domaine
    audit = db.query(Audit).filter(Audit.id_audit == audit_id).first()
    if not audit:
        raise HTTPException(status_code=404, detail=f"Audit {audit_id} non trouvé")

    domaine = db.query(Domaine).filter(Domaine.id_domaine == audit.id_domaine).first()
    if not domaine:
        raise HTTPException(
            status_code=404, detail=f"Domaine {audit.id_domaine} non trouvé"
        )

    # Statistiques globales
    stats = {
        "total_sous_domaines": db.query(SousDomaine)
        .filter(SousDomaine.id_domaine == domaine.id_domaine)
        .count(),
        "total_attaques": db.query(Attaque)
        .select_from(Attaque)
        .join(SousDomaine, Attaque.id_SD == SousDomaine.id_SD)
        .filter(SousDomaine.id_domaine == domaine.id_domaine)
        .count(),
        "total_failles": db.query(Faille)
        .select_from(Faille)
        .join(Attaque, Faille.id_attaque == Attaque.id_attaque)
        .join(SousDomaine, Attaque.id_SD == SousDomaine.id_SD)
        .filter(SousDomaine.id_domaine == domaine.id_domaine)
        .count(),
    }

    # Récupération des URLs vulnérables avec détails
    vulnerable_urls = (
        db.query(
            SousDomaine.url_SD,
            SousDomaine.description_SD,
            Type_attaque.nom_type,
            Attaque.payload,
            Attaque.date_attaque,
            Faille.balise,
            Faille.description,
            Faille.gravite,
        )
        .select_from(SousDomaine)
        .join(Attaque, SousDomaine.id_SD == Attaque.id_SD)
        .join(Type_attaque, Attaque.id_Type == Type_attaque.id_Type)
        .join(Faille, Attaque.id_attaque == Faille.id_attaque)
        .filter(SousDomaine.id_domaine == domaine.id_domaine)
        .order_by(SousDomaine.url_SD, Type_attaque.nom_type)
        .all()
    )

    # Toutes les URLs testées avec leur statut
    all_urls = (
        db.query(
            SousDomaine.url_SD,
            SousDomaine.description_SD,
            func.count(distinct(Attaque.id_attaque)).label("nb_attaques"),
            func.count(distinct(Faille.id_faille)).label("nb_failles"),
        )
        .select_from(SousDomaine)
        .outerjoin(Attaque, SousDomaine.id_SD == Attaque.id_SD)
        .outerjoin(Faille, Attaque.id_attaque == Faille.id_attaque)
        .filter(SousDomaine.id_domaine == domaine.id_domaine)
        .group_by(SousDomaine.url_SD, SousDomaine.description_SD)
        .order_by(SousDomaine.url_SD)
        .all()
    )
    return {
        "audit_info": {
            "id": audit_id,
            "date": audit.date,
            "domaine_principal": domaine.url_domaine,
            "description": domaine.description_domaine,
        },
        "statistics": stats,
        "vulnerable_urls": [
            {
                "url": url,
                "description": desc,
                "type_attaque": type_attaque,
                "payload": payload,
                "date_attaque": date_attaque,
                "balise": balise,
                "description_faille": faille_desc,
                "gravite": gravite,
            }
            for url, desc, type_attaque, payload, date_attaque, balise, faille_desc, gravite in vulnerable_urls
        ],
        "all_urls": [
            {
                "url": url,
                "description": desc,
                "nb_attaques": nb_attaques,
                "nb_failles": nb_failles,
                "is_vulnerable": nb_failles > 0,
            }
            for url, desc, nb_attaques, nb_failles in all_urls
        ],
    }


def rapport(audit_id: int, db: Session) -> bytes:
    """Service principal de génération de rapport"""
    try:
        data = get_audit_data(db, audit_id)
        return generer_rapport(data)

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de la génération du rapport: {str(e)}"
        )

def path_file(id_audit: int, db: Session) -> str:
    """Génère le chemin de téléchargement du rapport PDF"""
    audit = db.query(Audit).filter(Audit.id_audit == id_audit).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit non trouvé")
        
    domaine = db.query(Domaine).filter(Domaine.id_domaine == audit.id_domaine).first()
    if not domaine:
        raise HTTPException(status_code=404, detail="Domaine non trouvé")
        
    domaine_name = domaine.url_domaine
    domaine_name = domaine_name.replace("http://", "").replace("https://", "")
    domaine_name = domaine_name.replace(".", "-").replace(":", "-").replace("/", "-")
    
    return f"rapport-audit_id-{id_audit}_{domaine_name}.pdf"
    
