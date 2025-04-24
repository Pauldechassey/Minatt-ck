from typing import List
from sqlalchemy import select, union_all
from sqlalchemy.orm import Session
from app.models.sous_domaine import SousDomaine
import logging

logger = logging.getLogger(__name__)

def get_all_sous_domaines(db: Session):
    return db.query(SousDomaine).all()

def get_sous_domaine_by_id(sous_domaine_id: int, db: Session):
    return db.query(SousDomaine).filter(SousDomaine.id_SD == sous_domaine_id).first()
def get_sous_domaine_by_url(sous_domaine_url: str, db: Session):
    return db.query(SousDomaine).filter(SousDomaine.url_SD == sous_domaine_url).first()
    

def get_sous_domaines_by_domaine(domaine_id: int, db: Session):
    return db.query(SousDomaine).filter(SousDomaine.id_domaine == domaine_id).all()

def get_all_child_ids_recursively(initial_sous_domaine: SousDomaine, db: Session) -> List[int]:
    logger.info(f"Démarrage de la récupération récursive des sous-domaines enfants pour l'ID: {initial_sous_domaine.id_SD}")
    
    # Vérifier que le sous-domaine initial existe et est valide
    if not initial_sous_domaine:
        logger.error("Aucun sous-domaine fourni")
        raise ValueError("Aucun sous-domaine fourni")
        
    if not initial_sous_domaine.id_SD:
        logger.error(f"Le sous-domaine fourni n'a pas d'ID valide")
        raise ValueError(f"Le sous-domaine fourni n'a pas d'ID valide")
    
    logger.info(f"Sous-domaine initial validé avec ID: {initial_sous_domaine.id_SD}")
    
    try:
        all_ids = set([initial_sous_domaine.id_SD])  
        processed_ids = set() 
        
        ids_to_process = [initial_sous_domaine.id_SD]
        
        # Compteur de sécurité pour éviter une boucle infinie -> à enlever après validation des SDs
        safety_counter = 0
        max_iterations = 1000
        
        logger.info(f"Début du traitement avec l'ID initial: {initial_sous_domaine.id_SD} => {initial_sous_domaine.url_SD}")
        
        while ids_to_process and safety_counter < max_iterations:
            current_id = ids_to_process.pop(0)
            
            if current_id in processed_ids:
                continue
                            
            # Trouver tous les sous-domaines qui ont ce parent
            children = db.query(SousDomaine.id_SD).filter(
                SousDomaine.id_SD_Sous_domaine == current_id
            ).all()
            
            child_ids = [child[0] for child in children]
            logger.info(f"Enfants trouvés pour {current_id}: {child_ids}")
            
            # Ajouter uniquement les nouveaux IDs
            new_child_ids = [id for id in child_ids if id not in all_ids]
            
            all_ids.update(new_child_ids)
            ids_to_process.extend(new_child_ids)
            
            processed_ids.add(current_id)
            safety_counter += 1
                    
        if safety_counter >= max_iterations:
            logger.warning(f"Atteinte du nombre maximum d'itérations ({max_iterations}). Possible boucle infinie évitée.")
        
        logger.info(f"Tous les IDs récupérés: {list(all_ids)}")
        return list(all_ids)
            
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des sous-domaines: {str(e)}")
        raise