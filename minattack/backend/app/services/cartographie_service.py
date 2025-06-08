from sqlalchemy.orm import Session
import logging
import json
from typing import Dict, Any

from minattack.backend.app.models.audit import Audit
from minattack.backend.app.models.domaine import Domaine
from minattack.backend.app.models.sous_domaine import SousDomaine
from minattack.backend.app.models.technologie import Technologie
from minattack.backend.app.models.utiliser import Utiliser
from minattack.backend.app.models.vecteur import Vecteur
from minattack.backend.app.scripts.webcrawler import AsyncWebCrawler, run_async_crawler
from minattack.backend.app.services.domaine_service import get_domaine_by_id

logger = logging.getLogger(__name__)

def run_cartographie(audit: Audit, db: Session, fuzzing, wordlist_path) -> Dict[str, Any]:
    domaine = db.query(Domaine).filter(Domaine.id_domaine == audit.id_domaine).first()
    if not domaine:
        raise Exception(f"Domaine avec ID {audit.id_domaine} non trouvé")

    base_url = domaine.url_domaine
    logger.info(f"Début crawling pour le domaine: {base_url}")
    
    try:
        crawler = run_async_crawler(
            base_url=base_url,
            id_domaine=domaine.id_domaine,
            fuzzing=fuzzing,
            wordlist_path=wordlist_path,
        )
        logger.info("Fin crawling - Début sauvegarde en base")
        
        save_results = save_crawl_results_to_db(crawler, db, audit.id_audit)
        
        logger.info(f"Sauvegarde terminée: {save_results}")
        return save_results
        
    except Exception as e:
        logger.error(f"Erreur durant le crawling/sauvegarde: {e}")
        db.rollback()
        raise


def save_crawl_results_to_db(crawler: AsyncWebCrawler, db: Session, id_audit: int) -> Dict[str, Any]:
    
    stats = {
        'sous_domaines_saved': 0,
        'technologies_saved': 0,
        'vecteurs_saved': 0,
        'relations_utiliser_saved': 0,
        'errors': 0,
        'created_ids': {
            'sous_domaines': [],
            'technologies': [],
            'vecteurs': [],
            'utiliser': []
        }
    }
    
    try:
        # === 1. SAUVEGARDE DES SOUS-DOMAINES ===
        logger.info(f"Sauvegarde de {len(crawler.sous_domaines)} sous-domaines...")
        
        sd_id_mapping = {}  # Mapping ancien index -> nouvel ID en base
        
        for index, sous_domaine in enumerate(crawler.sous_domaines):
            try:
                # Vérifier si le sous-domaine existe déjà
                existing_sd = db.query(SousDomaine).filter(
                    SousDomaine.url_SD == sous_domaine.url_SD,
                    SousDomaine.id_domaine == sous_domaine.id_domaine
                ).first()
                
                if existing_sd:
                    logger.debug(f"Sous-domaine existant: {sous_domaine.url_SD}")
                    sd_id_mapping[index] = existing_sd.id_SD
                else:
                    # Gestion de la relation parent-enfant
                    parent_url = crawler.get_parent_url(sous_domaine.url_SD)
                    if parent_url:
                        # Trouver l'ID du parent en base
                        parent_sd = db.query(SousDomaine).filter(
                            SousDomaine.url_SD == parent_url,
                            SousDomaine.id_domaine == sous_domaine.id_domaine
                        ).first()
                        if parent_sd:
                            sous_domaine.id_SD_Sous_domaine = parent_sd.id_SD
                    
                    # Création du nouveau sous-domaine
                    new_sd = SousDomaine(
                        url_SD=sous_domaine.url_SD,
                        description_SD=sous_domaine.description_SD,
                        degre=sous_domaine.degre,
                        id_domaine=sous_domaine.id_domaine,
                        id_SD_Sous_domaine=sous_domaine.id_SD_Sous_domaine
                    )
                    
                    db.add(new_sd)
                    db.flush()  # Pour obtenir l'ID généré
                    
                    sd_id_mapping[index] = new_sd.id_SD
                    stats['created_ids']['sous_domaines'].append(new_sd.id_SD)
                    stats['sous_domaines_saved'] += 1
                    
                    logger.debug(f"Sous-domaine créé: {new_sd.url_SD} (ID: {new_sd.id_SD})")
                    
            except Exception as e:
                logger.error(f"Erreur sauvegarde sous-domaine {sous_domaine.url_SD}: {e}")
                stats['errors'] += 1
        
        # === 2. SAUVEGARDE DES TECHNOLOGIES ===
        logger.info(f"Sauvegarde de {len(crawler.technologies)} technologies...")
        
        tech_id_mapping = {}  # Mapping ancien index -> nouvel ID en base
        
        for index, technologie in enumerate(crawler.technologies):
            try:
                # Vérifier si la technologie existe déjà
                existing_tech = db.query(Technologie).filter(
                    Technologie.nom_techno == technologie.nom_techno,
                    Technologie.version_techno == technologie.version_techno
                ).first()
                
                if existing_tech:
                    logger.debug(f"Technologie existante: {technologie.nom_techno}")
                    tech_id_mapping[index] = existing_tech.id_techno
                else:
                    new_tech = Technologie(
                        nom_techno=technologie.nom_techno,
                        version_techno=technologie.version_techno
                    )
                    
                    db.add(new_tech)
                    db.flush()
                    
                    tech_id_mapping[index] = new_tech.id_techno
                    stats['created_ids']['technologies'].append(new_tech.id_techno)
                    stats['technologies_saved'] += 1
                    
                    logger.debug(f"Technologie créée: {new_tech.nom_techno} (ID: {new_tech.id_techno})")
                    
            except Exception as e:
                logger.error(f"Erreur sauvegarde technologie {technologie.nom_techno}: {e}")
                stats['errors'] += 1
        
        # === 3. SAUVEGARDE DES VECTEURS ===
        logger.info(f"Sauvegarde de {len(crawler.vecteurs)} vecteurs...")
        
        for vecteur in crawler.vecteurs:
            try:
                real_sd_id = None
                
                if hasattr(vecteur, 'id_SD') and vecteur.id_SD is not None:
                    if isinstance(vecteur.id_SD, int) and vecteur.id_SD in sd_id_mapping:
                        real_sd_id = sd_id_mapping.get(vecteur.id_SD)
                    else:
                        real_sd_id = vecteur.id_SD
                elif hasattr(vecteur, 'sd_index') and vecteur.sd_index is not None:
                    # Compatibilité avec l'ancien attribut
                    real_sd_id = sd_id_mapping.get(vecteur.sd_index)
                else:
                    logger.warning(f"Vecteur sans ID de sous-domaine valide")
                    continue
                
                if real_sd_id is None:
                    logger.warning(f"Impossible de trouver l'ID du sous-domaine pour le vecteur")
                    continue
                
                # un vecteur existe déjà pour ce sous-domaine?
                existing_vecteur = db.query(Vecteur).filter(
                    Vecteur.id_SD == real_sd_id
                ).first()
                
                if existing_vecteur:
                    # Mettre à jour le vecteur existant
                    existing_vecteur.vecteur = vecteur.vecteur
                    existing_vecteur.cluster = vecteur.cluster
                    logger.debug(f"Vecteur mis à jour pour SD ID: {real_sd_id}")
                    stats['vecteurs_saved'] += 1
                else:
                    # Créer un nouveau vecteur
                    new_vecteur = Vecteur(
                        vecteur=vecteur.vecteur,
                        cluster=vecteur.cluster,
                        id_SD=real_sd_id
                    )
                    
                    db.add(new_vecteur)
                    db.flush()
                    
                    stats['created_ids']['vecteurs'].append(new_vecteur.id_vecteur)
                    stats['vecteurs_saved'] += 1
                    
                    logger.debug(f"Vecteur créé pour SD ID: {real_sd_id}")
                    
            except Exception as e:
                logger.error(f"Erreur sauvegarde vecteur: {e}")
                logger.error(f"Détails vecteur: id_SD={getattr(vecteur, 'id_SD', 'N/A')}, sd_index={getattr(vecteur, 'sd_index', 'N/A')}")
                stats['errors'] += 1
        
        # === 4. SAUVEGARDE DES RELATIONS UTILISER ===
        logger.info(f"Sauvegarde de {len(crawler.relations_utiliser)} relations utiliser...")
    
        for utiliser_relation, tech_index in crawler.relations_utiliser:
            try:
                # Vérification plus robuste des types
                if not isinstance(tech_index, int):
                    logger.warning(f"tech_index n'est pas un entier: {tech_index} (type: {type(tech_index)})")
                    continue
                    
                # Récupérer l'ID réel de la technologie
                real_tech_id = tech_id_mapping.get(tech_index)
                if real_tech_id is None:
                    logger.warning(f"Impossible de trouver l'ID de la technologie (index: {tech_index})")
                    continue
                
                # Vérifier si la relation existe déjà
                existing_utiliser = db.query(Utiliser).filter(
                    Utiliser.id_domaine == utiliser_relation.id_domaine,
                    Utiliser.id_techno == real_tech_id
                ).first()
                
                if not existing_utiliser:
                    new_utiliser = Utiliser(
                        id_domaine=utiliser_relation.id_domaine,
                        id_techno=real_tech_id
                    )
                    
                    db.add(new_utiliser)
                    db.flush()
                    
                    try:
                        utiliser_id = new_utiliser.id_utiliser if hasattr(new_utiliser, 'id_utiliser') else "N/A"
                        stats['created_ids']['utiliser'].append(utiliser_id)
                    except AttributeError:
                        # Si l'attribut n'existe pas, ignorez-le
                        pass
                        
                    stats['relations_utiliser_saved'] += 1
                    
                    logger.debug(f"Relation Utiliser créée: Domaine {utiliser_relation.id_domaine} -> Tech {real_tech_id}")
                else:
                    logger.debug(f"Relation Utiliser existante: Domaine {utiliser_relation.id_domaine} -> Tech {real_tech_id}")
                    
            except Exception as e:
                logger.error(f"Erreur sauvegarde relation utiliser: {e}")
                stats['errors'] += 1
        
        # === COMMIT FINAL ===
        db.commit()
        logger.info("Toutes les données ont été sauvegardées avec succès")
        
        # === STATISTIQUES FINALES ===
        stats['crawler_stats'] = crawler.stats
        stats['total_urls_crawled'] = len(crawler.visited_urls)
        stats['hierarchy_depth'] = len(crawler.parent_child_map)
        
        return stats
        
    except Exception as e:
        logger.error(f"Erreur globale lors de la sauvegarde: {e}")
        db.rollback()
        stats['errors'] += 1
        raise

