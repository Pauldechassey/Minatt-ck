from http.client import HTTPException
from typing import List, Dict
from datetime import datetime
from sqlalchemy.orm import Session
import logging

from minattack.backend.app.scripts.attaque_script import AttaqueScript
from minattack.backend.app.models.sous_domaine import SousDomaine
from minattack.backend.app.services.sous_domaine_service import get_all_child_ids_recursively, get_sous_domaine_by_id
from minattack.backend.app.models.attaque import Attaque
from minattack.backend.app.models.faille import Faille
from minattack.backend.app.models.type_attaque import Type_attaque


logger = logging.getLogger(__name__)



def run_attacks(SD_initial_id: int, attaque_type: List[str], db: Session, single: bool = False) -> bool:  
    
    attaque = AttaqueScript()
    SD_initial = get_sous_domaine_by_id(SD_initial_id, db)
    if not SD_initial:
        logger.error("Sous-domaine initial non trouvé")
        raise HTTPException(status_code=404, detail="Sous-domaine initial non trouvé")
    
    logger.info(f"Sous-domaine initial trouvé : {SD_initial.url_SD}")
    
    SD_cibles_id = (
        get_all_child_ids_recursively(SD_initial, db)
        if not single else
        [SD_initial_id]
    )

    if single:
        logger.info(f"Attaque sur le sous-domaine initial uniquement : {SD_initial.url_SD}")
    else:
        logger.info(f"{len(SD_cibles_id)} sous-domaines cibles trouvés pour l'attaque.")

    urls_traitees = 0

    for sous_domaine_id in SD_cibles_id:
        sous_domaine = get_sous_domaine_by_id(sous_domaine_id, db)
        if not sous_domaine:
            #logger.warning(f"Sous-domaine cible avec ID {sous_domaine_id} non trouvé.")
            continue
        
        logger.info(f"Lancement de l'attaque sur : {sous_domaine.url_SD}")
        save_attacks(sous_domaine, attaque.run_attack(sous_domaine, attaque_type), db)
        logger.info(f"Attaque terminée sur : {sous_domaine.url_SD}")
        urls_traitees += 1

    return urls_traitees == len(SD_cibles_id)

    
        

def save_attacks(SD_cible: SousDomaine, resultats: Dict[str, List], db: Session):
    types_attaques = {
        "sqli": 1,
        "xss": 2,
        "csrf": 3,
        "headers_cookies": 4
    }
    
    #logger.info(f"Début de la sauvegarde des attaques pour le sous-domaine {SD_cible.id_SD}")
    
    try:
        for type_attaque, type_id in types_attaques.items(): 
            #logger.info(f"Traitement du type d'attaque: {type_attaque} (ID: {type_id})")
            
            result_attaque = resultats.get(type_attaque, {})
            if not result_attaque:
                continue
                        
            # Vérifier si result_attaque est un dictionnaire ou une liste
            if isinstance(result_attaque, dict):
                attaques = result_attaque.get("attaques", [])
                failles = result_attaque.get("failles", [])
            else:
                # Si c'est une liste, supposons que ce sont des attaques sans failles
                attaques = result_attaque
                failles = []
                        
            type_obj = db.query(Type_attaque).get(type_id)
            if not type_obj:
                #logger.warning(f"Type d'attaque non trouvé dans la BDD : {type_attaque}")
                continue
            
            attaque_mapping = {}
            
            for attaque_data in attaques:
                #logger.info(f"Traitement de l'attaque: {attaque_data}")
                
                nouvelle_attaque = Attaque(
                    payload=attaque_data.payload if hasattr(attaque_data, 'payload') else str(attaque_data),
                    date_attaque=attaque_data.date_attaque if hasattr(attaque_data, 'date_attaque') else datetime.now(),
                    resultat=attaque_data.resultat if hasattr(attaque_data, 'resultat') else None,
                    id_SD=SD_cible.id_SD,
                    id_Type=type_obj.id_Type
                )
                
                db.add(nouvelle_attaque)
                db.flush()
                
                if hasattr(attaque_data, 'id_provisoire'):
                    attaque_mapping[attaque_data.id_provisoire] = nouvelle_attaque.id_attaque
            
            for faille_data in failles:
                if hasattr(faille_data, 'id_provisoire') and faille_data.id_provisoire in attaque_mapping:
                    #logger.info(f"Traitement de la faille liée à l'attaque {faille_data.id_provisoire}")
                    
                    nouvelle_faille = Faille(
                        gravite=faille_data.gravite,
                        description=faille_data.description,
                        balise=faille_data.balise,
                        id_attaque=attaque_mapping[faille_data.id_provisoire]
                    )
                    db.add(nouvelle_faille)
            
            try:
                db.commit()
                #logger.info(f"Sauvegarde réussie pour les attaques de type {type_attaque}")
            except Exception as e:
                db.rollback()
                #logger.error(f"Erreur lors de la sauvegarde des attaques {type_attaque}: {str(e)}")
                #logger.exception("Détails de l'erreur:")
                raise
        
    except Exception as e:
        db.rollback()
        #logger.error(f"Erreur générale lors de la sauvegarde: {str(e)}")
        #logger.exception("Détails de l'erreur:")
        raise
    
    finally:
        # S'assurer que toutes les modifications sont bien enregistrées
        db.commit()
        #logger.info("Fin de la sauvegarde des attaques")