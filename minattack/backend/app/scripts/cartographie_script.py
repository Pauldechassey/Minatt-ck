from minattack.backend.app.scripts.webcrawler import WebCrawler
import logging

logger = logging.getLogger(__name__)

def run_cartographie(base_url: str, db, id_audit=None, id_domaine=None) -> bool:
    """
    Exécute la cartographie en utilisant BFS à partir d'une URL de base.
    
    Args:
        base_url (str): L'URL du domaine racine
        db: Session de base de données
        id_audit (int, optional): ID de l'audit associé
        id_domaine (int, optional): ID du domaine dans la BDD
        
    Returns:
        bool: True si la cartographie a réussi, False sinon
    """
    logger.info(f"Début du crawling BFS pour {base_url} (Audit ID: {id_audit}, Domaine ID: {id_domaine})")
    
    try:
        crawler = WebCrawler(base_url, id_audit=id_audit, id_domaine=id_domaine)
        
        crawler.crawl_bfs()
        
        logger.info(f"Crawling terminé, {len(crawler.sous_domaines)} sous-domaines trouvés")
        logger.info(f"Vecteurs générés: {len(crawler.vecteurs)}")
        
        # Trier les sous-domaines par degré pour maintenir l'ordre BFS
        crawler.sous_domaines.sort(key=lambda sd: (sd.degre, sd.url_SD))
        
        nb_sd = 0
        nb_techs = 0
        nb_vecteurs = 0
        tech_ids = {}  # Pour stocker les IDs des technologies après l'ajout en BDD
        
        parent_map = {}  # Pour stocker la correspondance index -> id_SD après le flush
        
        # === 1. SAUVEGARDE DES SOUS-DOMAINES ===
        logger.info("Sauvegarde des sous-domaines...")
        for i, sd in enumerate(crawler.sous_domaines):
            db.add(sd)
            db.flush()  # Flush pour obtenir l'ID généré
            parent_map[i] = sd.id_SD
            nb_sd += 1
            logger.debug(f"Sous-domaine ajouté: {sd.url_SD} (ID: {sd.id_SD}, degré: {sd.degre})")
        
        # === 2. MISE À JOUR DES RELATIONS PARENT-ENFANT ===
        logger.info("Mise à jour des relations parent-enfant...")
        for i, sd in enumerate(crawler.sous_domaines):
            if i > 0:  # Ignorer la racine
                # Trouver l'URL parent et récupérer son ID de la BDD
                parent_url = None
                for url, index in crawler.url_to_sd_id.items():
                    if index == i and sd.id_SD_Sous_domaine is not None:
                        # Trouver l'URL parent dans la structure
                        for parent_url_candidate, parent_index in crawler.url_to_sd_id.items():
                            if parent_index == sd.id_SD_Sous_domaine:
                                parent_url = parent_url_candidate
                                break
                        break
                
                if parent_url and parent_url in crawler.url_to_sd_id:
                    parent_index = crawler.url_to_sd_id[parent_url]
                    parent_id = parent_map.get(parent_index)
                    if parent_id:
                        sd.id_SD_Sous_domaine = parent_id
                        db.merge(sd)
        
        # === 3. SAUVEGARDE DES VECTEURS ===
        logger.info("Sauvegarde des vecteurs...")
        for vecteur in crawler.vecteurs:
            # Récupérer l'ID réel du sous-domaine grâce au mapping
            sd_index = getattr(vecteur, 'sd_index', None)
            if sd_index is not None and sd_index in parent_map:
                vecteur.id_SD = parent_map[sd_index]
                # Supprimer l'attribut temporaire
                delattr(vecteur, 'sd_index')
                
                db.add(vecteur)
                db.flush()
                nb_vecteurs += 1
                logger.debug(f"Vecteur ajouté pour sous-domaine ID: {vecteur.id_SD}")
            else:
                logger.warning(f"Impossible de mapper le vecteur avec l'index {sd_index}")
        
        # === 4. SAUVEGARDE DES TECHNOLOGIES ===
        logger.info("Sauvegarde des technologies...")
        for i, tech in enumerate(crawler.technologies):
            db.add(tech)
            db.flush()
            tech_ids[i] = tech.id_techno
            nb_techs += 1
            logger.debug(f"Technologie ajoutée: {tech.nom_techno} v{tech.version_techno} (ID: {tech.id_techno})")
        
        # === 5. SAUVEGARDE DES RELATIONS UTILISER ===
        logger.info("Sauvegarde des relations Utiliser...")
        for utiliser, tech_index in crawler.relations_utiliser:
            utiliser.id_techno = tech_ids.get(tech_index)
            if utiliser.id_techno:
                db.add(utiliser)
                db.flush()
                logger.debug(f"Relation ajoutée: Domaine {utiliser.id_domaine} utilise Techno {utiliser.id_techno}")
        
        # === 6. COMMIT FINAL ===
        db.commit()
        
        logger.info(f"Cartographie terminée avec succès:")
        logger.info(f"  - Sous-domaines sauvegardés: {nb_sd}")
        logger.info(f"  - Vecteurs sauvegardés: {nb_vecteurs}")
        logger.info(f"  - Technologies sauvegardées: {nb_techs}")
        logger.info(f"  - Relations Utiliser créées: {len(crawler.relations_utiliser)}")
        
        # Valider la réussite du processus
        success = (
            nb_sd == len(crawler.sous_domaines) and 
            nb_techs == len(crawler.technologies) and
            nb_vecteurs == len(crawler.vecteurs)
        )
        
        if not success:
            logger.warning(f"Incohérence détectée: SD attendus={len(crawler.sous_domaines)}, sauvegardés={nb_sd}")
            logger.warning(f"Vecteurs attendus={len(crawler.vecteurs)}, sauvegardés={nb_vecteurs}")
        
        return success
        
    except Exception as e:
        logger.error(f"Erreur lors de la cartographie: {e}")
        db.rollback()
        return False