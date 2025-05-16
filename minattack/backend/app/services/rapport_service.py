from fastapi import HTTPException
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
from rapport_service import generer_rapport

def get_audit_data(db: Session, audit_id: int) -> Dict:
    """Récupère toutes les données nécessaires pour le rapport"""
    
    # Vérification/récupération audit et domaine
    audit = db.query(Audit).filter(Audit.id_audit == audit_id).first()
    if not audit:
        raise HTTPException(status_code=404, detail=f"Audit {audit_id} non trouvé")

    domaine = db.query(Domaine).filter(Domaine.id_domaine == audit.id_domaine).first()
    if not domaine:
        raise HTTPException(status_code=404, detail=f"Domaine {audit.id_domaine} non trouvé")

    # Statistiques globales
    stats = {
        "total_sous_domaines": db.query(SousDomaine)
            .filter(SousDomaine.id_domaine == domaine.id_domaine)
            .count(),
        "total_attaques": db.query(Attaque)
            .join(SousDomaine)
            .filter(SousDomaine.id_domaine == domaine.id_domaine)
            .count(),
        "total_failles": db.query(Faille)
            .join(Attaque)
            .join(SousDomaine)
            .filter(SousDomaine.id_domaine == domaine.id_domaine)
            .count()
    }

    # Récupération des URLs vulnérables avec détails
    vulnerable_urls = db.query(
        SousDomaine.url_SD,
        SousDomaine.description_SD,
        Type_attaque.nom_type,
        Attaque.payload,
        Attaque.date_attaque,
        Faille.balise,
        Faille.description,
        Faille.gravite
    ).join(Attaque
    ).join(Type_attaque, Attaque.id_Type == Type_attaque.id_Type
    ).join(Faille
    ).filter(SousDomaine.id_domaine == domaine.id_domaine
    ).order_by(SousDomaine.url_SD, Type_attaque.nom_type).all()

    # Toutes les URLs testées avec leur statut
    all_urls = db.query(
        SousDomaine.url_SD,
        SousDomaine.description_SD,
        func.count(distinct(Attaque.id_attaque)).label('nb_attaques'),
        func.count(distinct(Faille.id_faille)).label('nb_failles')
    ).outerjoin(Attaque
    ).outerjoin(Faille
    ).filter(SousDomaine.id_domaine == domaine.id_domaine
    ).group_by(SousDomaine.url_SD, SousDomaine.description_SD
    ).order_by(SousDomaine.url_SD).all()

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
                "gravite": gravite
            } for url, desc, type_attaque, payload, date_attaque, balise, faille_desc, gravite in vulnerable_urls
        ],
        "all_urls": [
            {
                "url": url,
                "description": desc,
                "nb_attaques": nb_attaques,
                "nb_failles": nb_failles,
                "is_vulnerable": nb_failles > 0
            } for url, desc, nb_attaques, nb_failles in all_urls
        ]
    }

def rapport(audit_id: int, db: Session) -> Dict:
    """Service principal de génération de rapport"""
    try:
        # Récupérer les données
        data = get_audit_data(db, audit_id)
        
        # Générer le PDF
        pdf_result = generer_rapport(data)
        
        return {
            "status": "success",
            "message": "Rapport généré avec succès",
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération du rapport: {str(e)}"
        )

