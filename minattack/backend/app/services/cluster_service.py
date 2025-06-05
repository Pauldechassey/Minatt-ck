import json
from typing import List, Tuple
from sqlalchemy.orm import Session
from minattack.backend.app.models.domaine import Domaine
from minattack.backend.app.models.sous_domaine import SousDomaine
from minattack.backend.app.models.vecteur import Vecteur
import logging

logger = logging.getLogger(__name__)

def get_vectors_from_sd_initial(db: Session, sd_initial_id: int) -> Tuple[List[int], List[list]]:
    """
    Récupère tous les vecteurs du même domaine que le sous-domaine initial.
    
    Args:
        db: Session de base de données
        sd_initial_id: ID du sous-domaine initial
        
    Returns:
        Tuple[List[int], List[list]]: (liste des id_SD, liste des vecteurs)
    """
    try:
        # Récupérer le sous-domaine initial
        sd_initial = db.query(SousDomaine).filter(SousDomaine.id_SD == sd_initial_id).first()
        
        if not sd_initial:
            logger.error(f"Sous-domaine initial {sd_initial_id} non trouvé")
            return [], []
        
        logger.info(f"Sous-domaine initial trouvé: {sd_initial.url_SD}")
        
        # Récupérer tous les sous-domaines du même domaine
        tous_sous_domaines = (
            db.query(SousDomaine)
            .filter(SousDomaine.id_domaine == sd_initial.id_domaine)
            .all()
        )
        
        if not tous_sous_domaines:
            logger.warning(f"Aucun sous-domaine trouvé pour le domaine {sd_initial.id_domaine}")
            return [], []
        
        # Extraire les IDs des sous-domaines
        sous_domaine_ids = [sd.id_SD for sd in tous_sous_domaines]
        logger.info(f"Nombre de sous-domaines dans le domaine: {len(sous_domaine_ids)}")
        
        # Récupérer les vecteurs correspondants
        vecteurs = (
            db.query(Vecteur)
            .filter(Vecteur.id_SD.in_(sous_domaine_ids))
            .all()
        )
        
        if not vecteurs:
            logger.warning(f"Aucun vecteur trouvé pour les sous-domaines du domaine")
            return [], []
        
        # Extraire les données
        ids = [v.id_SD for v in vecteurs]
        vectors = []
        
        for v in vecteurs:
            try:
                # Désérialiser le JSON du vecteur
                if isinstance(v.vecteur, str):
                    vector_data = json.loads(v.vecteur)
                else:
                    vector_data = v.vecteur
                
                vectors.append(vector_data)
                
            except (json.JSONDecodeError, TypeError) as e:
                logger.error(f"Erreur lors de la désérialisation du vecteur {v.id_vecteur}: {e}")
                continue
        
        logger.info(f"Récupération réussie: {len(ids)} vecteurs pour le domaine du SD {sd_initial_id}")
        return ids, vectors
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des vecteurs pour SD {sd_initial_id}: {e}")
        return [], []


def validate_vectors(vectors: List[list]) -> bool:
    """
    Valide que tous les vecteurs ont la même dimension et sont valides.
    
    Args:
        vectors: Liste des vecteurs à valider
        
    Returns:
        bool: True si tous les vecteurs sont valides
    """
    if not vectors:
        return False
    
    # Vérifier que tous les vecteurs ont la même longueur
    expected_length = len(vectors[0])
    
    for i, vector in enumerate(vectors):
        if not isinstance(vector, list):
            logger.error(f"Vecteur {i} n'est pas une liste: {type(vector)}")
            return False
        
        if len(vector) != expected_length:
            logger.error(f"Vecteur {i} a une longueur incorrecte: {len(vector)} != {expected_length}")
            return False
        
        # Vérifier que tous les éléments sont numériques
        for j, val in enumerate(vector):
            if not isinstance(val, (int, float)):
                logger.error(f"Vecteur {i}, élément {j} n'est pas numérique: {val}")
                return False
    
    logger.info(f"Validation réussie: {len(vectors)} vecteurs de dimension {expected_length}")
    return True