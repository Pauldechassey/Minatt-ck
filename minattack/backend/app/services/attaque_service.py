from http.client import HTTPException
from typing import List, Dict
from datetime import datetime
from sqlalchemy.orm import Session
import logging

from minattack.backend.app.scripts.classification_DBSCAN_script import classification_DBSCAN
from minattack.backend.app.scripts.attaque_script import AttaqueScript
from minattack.backend.app.models.sous_domaine import SousDomaine
from minattack.backend.app.services.audit_service import get_audit_by_id
from minattack.backend.app.services.cluster_service import get_vectors_from_sd_initial, validate_vectors
from minattack.backend.app.services.embedder_service import Embedder
from minattack.backend.app.services.sous_domaine_service import (
    get_all_child_ids_recursively,
    get_sous_domaine_by_id,
    get_sous_domaines_by_domaine,
)
from minattack.backend.app.models.attaque import Attaque
from minattack.backend.app.models.faille import Faille
from minattack.backend.app.models.type_attaque import Type_attaque
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np

logger = logging.getLogger(__name__)


def run_attacks(id_audit: int, attaque_type: List[str], db: Session, single: bool = False) -> bool:
    id_domaine = get_audit_by_id(id_audit, db).id_domaine
    if not id_domaine:
        logger.error(f"Audit avec ID {id_audit} non trouvé")
        raise HTTPException(status_code=404, detail=f"Audit avec ID {id_audit} non trouvé")
    sous_domaines = get_sous_domaines_by_domaine(id_domaine, db)
    
    id_sous_domaine_initial = None
    for sd in sous_domaines:
        if sd.degre == 0:  # Sous-domaine racine
            id_sous_domaine_initial = sd.id_SD
            break
    
    if not id_sous_domaine_initial:
        logger.error(f"Sous-domaine initial non trouvé pour l'audit ID {id_audit}")
        raise HTTPException(status_code=404, detail=f"Sous-domaine initial non trouvé pour l'audit ID {id_audit}")
    
    attaque = AttaqueScript()
    SD_initial = get_sous_domaine_by_id(id_sous_domaine_initial, db)
    if not SD_initial:
        logger.error("Sous-domaine initial non trouvé")
        raise HTTPException(status_code=404, detail="Sous-domaine initial non trouvé")

    logger.info(f"Sous-domaine initial trouvé : {SD_initial.url_SD}")

    SD_cibles_id = get_all_child_ids_recursively(SD_initial, db) if not single else [SD_initial.id_SD]

    if single:
        logger.info(f"Attaque sur le sous-domaine initial uniquement : {SD_initial.url_SD}")
    else:
        logger.info(f"{len(SD_cibles_id)} sous-domaines cibles trouvés pour l'attaque.")

    urls_traitees = 0

    for sous_domaine_id in SD_cibles_id:
        sous_domaine = get_sous_domaine_by_id(sous_domaine_id, db)
        if not sous_domaine:
            logger.warning(f"Sous-domaine cible avec ID {sous_domaine_id} non trouvé.")
            continue

        logger.info(f"Lancement de l'attaque sur : {sous_domaine.url_SD}")
        save_attacks(sous_domaine, attaque.run_attack(sous_domaine, attaque_type), db)
        logger.info(f"Attaque terminée sur : {sous_domaine.url_SD}")
        urls_traitees += 1

    return urls_traitees == len(SD_cibles_id)


def run_cluster_attacks(id_audit: int, attaque_type: List[str], db: Session) -> bool:
    """
    Lance des attaques basées sur le clustering des sous-domaines.
    
    Args:
        SD_initial_id: ID du sous-domaine initial
        attaque_type: Types d'attaques à lancer
        db: Session de base de données
        use_hierarchy: Si True, utilise la hiérarchie, sinon utilise le domaine complet
        
    Returns:
        bool: True si toutes les attaques ont réussi
    """
    id_domaine = get_audit_by_id(id_audit, db).id_domaine
    if not id_domaine:
        logger.error(f"Audit avec ID {id_audit} non trouvé")
        raise HTTPException(status_code=404, detail=f"Audit avec ID {id_audit} non trouvé")
    
    sous_domaines = get_sous_domaines_by_domaine(id_domaine, db)
    
    id_sous_domaine_initial = None
    for sd in sous_domaines:
        if sd.degre == 0:  # Sous-domaine racine
            id_sous_domaine_initial = sd.id_SD
            break
    
    if not id_sous_domaine_initial:
        logger.error(f"Sous-domaine initial non trouvé pour l'audit ID {id_audit}")
        raise HTTPException(status_code=404, detail=f"Sous-domaine initial non trouvé pour l'audit ID {id_audit}")
    
    # Récupération des vecteurs
    
    ids, vectors = get_vectors_from_sd_initial(db, sd_initial_id=id_sous_domaine_initial)

    if len(ids)<15:
        logger.warning(f"Nombre de sous-domaines ({len(ids)}) trop faible pour le clustering, utilisation de l'attaque directe")
        return run_attacks(id_audit, attaque_type, db, False)

    if not ids or not vectors:
        logger.error("Aucun vecteur récupéré")
        return False
    
    # Validation des vecteurs
    if not validate_vectors(vectors):
        logger.error("Vecteurs invalides")
        return False
    
    if any(v is None for v in vectors):
        logger.error("Certains vecteurs sont vides ou non valides.")
        return False

    logger.info(f"Nombre de vecteurs récupérés: {len(vectors)}")

    # Embedding
    try:
        embedder = Embedder(vectors)
        embedded_vectors = [embedder.embed(v) for v in vectors]
        logger.info(f"Embedding terminé: {len(embedded_vectors)} vecteurs embeddés")
    except Exception as e:
        logger.error(f"Erreur lors de l'embedding: {e}")
        return False

    # Clustering
    try:
        labels = classification_DBSCAN(embedded_vectors, save_plot=True)
        if labels is None or len(labels) == 0:
            logger.error("Échec du clustering DBSCAN")
            return False
        
        logger.info(f"Clustering terminé: {len(set(labels))} clusters trouvés")
    except Exception as e:
        logger.error(f"Erreur lors du clustering: {e}")
        return False
    
    cluster_dict = {}  # cluster_id -> list of (id_SD, vector_embedded)
    outsider_ids = []  # Pour les sous-domaines qui ne sont pas dans un cluster

    for id_sd, label, vec in zip(ids, labels, embedded_vectors):
        if label == -1:
            outsider_ids.append(id_sd)
            logger.info(f"Sous-domaine {id_sd} considéré comme outsider (label -1)")
        else:
            cluster_dict.setdefault(label, []).append((id_sd, vec))

    # Vérification de cohérence
    total_processed = sum(len(sd_list) for sd_list in cluster_dict.values()) + len(outsider_ids)
    if total_processed != len(ids):
        logger.error(f"Erreur dans la classification des clusters : {total_processed} != {len(ids)}")
        raise HTTPException(status_code=500, detail="Erreur dans la classification des clusters")

    logger.info(f"Répartition des clusters:")
    logger.info(f"  - Nombre de clusters: {len(cluster_dict)}")
    logger.info(f"  - Outsiders: {len(outsider_ids)}")
    for cluster_id, sd_list in cluster_dict.items():
        if cluster_id != -1:  # Ignorer les outsiders déjà comptés
            logger.info(f"  - Cluster {cluster_id}: {len(sd_list)} sous-domaines")

    urls_traitees = 0
    attack_cluster = AttaqueScript()
    
    # Lancer attaque sur chaque centre de cluster
    for cluster_id, sd_list in cluster_dict.items():
        if not sd_list or cluster_id == -1:  # Ignorer les clusters vides et les outsiders
            continue
            
        logger.info(f"Traitement du cluster {cluster_id} avec {len(sd_list)} sous-domaines")
        
        # Calcul du centre géométrique
        center_vector = np.mean([vec for _, vec in sd_list], axis=0)

        # Trouver le sous-domaine le plus proche du centre
        min_dist = float("inf")
        center_sd_id = None
        for sd_id, vec in sd_list:
            dist = np.linalg.norm(center_vector - vec)
            if dist < min_dist:
                min_dist = dist
                center_sd_id = sd_id
                
        logger.info(f"Centre du cluster {cluster_id} trouvé : ID {center_sd_id} (distance: {min_dist:.4f})")

        # Attaquer le centre du cluster
        sous_domaine = get_sous_domaine_by_id(center_sd_id, db)
        if not sous_domaine:
            logger.warning(f"Sous-domaine centre {center_sd_id} non trouvé")
            continue

        logger.info(f"Lancement de l'attaque sur le centre du cluster {cluster_id} -- sous-domaine : {sous_domaine.url_SD}")
        
        try:
            result_cluster = attack_cluster.run_attack(sous_domaine, attaque_type)
            save_attacks(sous_domaine, result_cluster, db)
            urls_traitees += 1
            
            # Appliquer le résultat aux autres membres du cluster
            for id_sd, _ in sd_list:
                if id_sd != center_sd_id:
                    sd = get_sous_domaine_by_id(id_sd, db)
                    if sd:
                        logger.info(f"Application des résultats du centre au sous-domaine {sd.url_SD}")
                        save_attacks(sd, result_cluster, db)
                        urls_traitees += 1
                        
        except Exception as e:
            logger.error(f"Erreur lors de l'attaque du cluster {cluster_id}: {e}")
            continue

    # Traiter les outsiders individuellement
    logger.info(f"Traitement de {len(outsider_ids)} outsiders")
    for outsider_id in outsider_ids:
        sous_domaine = get_sous_domaine_by_id(outsider_id, db)
        if not sous_domaine:
            logger.warning(f"Sous-domaine outsider {outsider_id} non trouvé")
            continue

        logger.info(f"Lancement de l'attaque sur l'outsider : {sous_domaine.url_SD}")
        try:
            save_attacks(sous_domaine, attack_cluster.run_attack(sous_domaine, attaque_type), db)
            urls_traitees += 1
        except Exception as e:
            logger.error(f"Erreur lors de l'attaque de l'outsider {outsider_id}: {e}")
            continue
    
    logger.info(f"Attaques terminées: {urls_traitees}/{len(ids)} sous-domaines traités")
    return urls_traitees == len(ids)


def save_attacks(SD_cible: SousDomaine, resultats: Dict[str, List], db: Session):
    types_attaques = {"sqli": 1, "xss": 2, "csrf": 3, "headers_cookies": 4}

    # logger.info(f"Début de la sauvegarde des attaques pour le sous-domaine {SD_cible.id_SD}")

    try:
        for type_attaque, type_id in types_attaques.items():
            # logger.info(f"Traitement du type d'attaque: {type_attaque} (ID: {type_id})")

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
                # logger.warning(f"Type d'attaque non trouvé dans la BDD : {type_attaque}")
                continue

            attaque_mapping = {}

            for attaque_data in attaques:
                # logger.info(f"Traitement de l'attaque: {attaque_data}")

                nouvelle_attaque = Attaque(
                    payload=(attaque_data.payload if hasattr(attaque_data, "payload") else str(attaque_data)),
                    date_attaque=(attaque_data.date_attaque if hasattr(attaque_data, "date_attaque") else datetime.now()),
                    resultat=(attaque_data.resultat if hasattr(attaque_data, "resultat") else None),
                    id_SD=SD_cible.id_SD,
                    id_Type=type_obj.id_Type,
                )

                db.add(nouvelle_attaque)
                db.flush()

                if hasattr(attaque_data, "id_provisoire"):
                    attaque_mapping[attaque_data.id_provisoire] = nouvelle_attaque.id_attaque

            for faille_data in failles:
                if hasattr(faille_data, "id_provisoire") and faille_data.id_provisoire in attaque_mapping:
                    # logger.info(f"Traitement de la faille liée à l'attaque {faille_data.id_provisoire}")

                    nouvelle_faille = Faille(
                        gravite=faille_data.gravite,
                        description=faille_data.description,
                        balise=faille_data.balise,
                        id_attaque=attaque_mapping[faille_data.id_provisoire],
                    )
                    db.add(nouvelle_faille)

            try:
                db.commit()
                # logger.info(f"Sauvegarde réussie pour les attaques de type {type_attaque}")
            except Exception as e:
                db.rollback()
                # logger.error(f"Erreur lors de la sauvegarde des attaques {type_attaque}: {str(e)}")
                # logger.exception("Détails de l'erreur:")
                raise

    except Exception as e:
        db.rollback()
        # logger.error(f"Erreur générale lors de la sauvegarde: {str(e)}")
        # logger.exception("Détails de l'erreur:")
        raise

    finally:
        db.commit()
        # logger.info("Fin de la sauvegarde des attaques")