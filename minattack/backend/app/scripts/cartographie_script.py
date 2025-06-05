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
        
        # Dictionnaire pour mapper URL -> ID en base de données
        url_to_db_id = {}
        
        # === 1. SAUVEGARDE DES SOUS-DOMAINES EN ORDRE BFS ===
        logger.info("Sauvegarde des sous-domaines...")
        for sd in crawler.sous_domaines:
            # Trouver l'ID du parent en base de données
            parent_db_id = None
            if sd.degre > 0:  # Pas la racine
                # Chercher le parent dans url_to_db_id grâce au mapping du crawler
                parent_url = crawler.get_parent_url(sd.url_SD)
                if parent_url and parent_url in url_to_db_id:
                    parent_db_id = url_to_db_id[parent_url]
                    logger.debug(f"Parent trouvé pour {sd.url_SD}: {parent_url} (ID: {parent_db_id})")
                else:
                    logger.warning(f"Parent non trouvé pour {sd.url_SD}")
            
            # Mettre à jour l'ID du parent
            sd.id_SD_Sous_domaine = parent_db_id
            
            # Sauvegarder en base
            db.add(sd)
            db.flush()  # Flush pour obtenir l'ID généré
            
            # Mapper l'URL vers l'ID en base de données
            url_to_db_id[sd.url_SD] = sd.id_SD
            nb_sd += 1
            
            logger.debug(f"Sous-domaine ajouté: {sd.url_SD} (ID: {sd.id_SD}, Parent ID: {parent_db_id}, degré: {sd.degre})")
        
        # === 2. SAUVEGARDE DES VECTEURS ===
        logger.info("Sauvegarde des vecteurs...")
        for vecteur in crawler.vecteurs:
            # Récupérer l'URL du sous-domaine correspondant
            sd_index = getattr(vecteur, 'sd_index', None)
            if sd_index is not None and sd_index < len(crawler.sous_domaines):
                sd_url = crawler.sous_domaines[sd_index].url_SD
                # Récupérer l'ID réel du sous-domaine
                if sd_url in url_to_db_id:
                    vecteur.id_SD = url_to_db_id[sd_url]
                    # Supprimer l'attribut temporaire
                    delattr(vecteur, 'sd_index')
                    
                    db.add(vecteur)
                    db.flush()
                    nb_vecteurs += 1
                    logger.debug(f"Vecteur ajouté pour sous-domaine {sd_url} (ID: {vecteur.id_SD})")
                else:
                    logger.warning(f"URL {sd_url} non trouvée dans le mapping")
            else:
                logger.warning(f"Index de sous-domaine invalide: {sd_index}")
        
        # === 3. SAUVEGARDE DES TECHNOLOGIES ===
        logger.info("Sauvegarde des technologies...")
        for i, tech in enumerate(crawler.technologies):
            db.add(tech)
            db.flush()
            tech_ids[i] = tech.id_techno
            nb_techs += 1
            logger.debug(f"Technologie ajoutée: {tech.nom_techno} v{tech.version_techno} (ID: {tech.id_techno})")
        
        # === 4. SAUVEGARDE DES RELATIONS UTILISER ===
        logger.info("Sauvegarde des relations Utiliser...")
        for utiliser, tech_index in crawler.relations_utiliser:
            utiliser.id_techno = tech_ids.get(tech_index)
            if utiliser.id_techno:
                db.add(utiliser)
                db.flush()
                logger.debug(f"Relation ajoutée: Domaine {utiliser.id_domaine} utilise Techno {utiliser.id_techno}")
        
        # === 5. COMMIT FINAL ===
        db.commit()
        
        # === 6. VÉRIFICATION DES RELATIONS PARENT-ENFANT ===
        logger.info("Vérification des relations parent-enfant...")
        for sd in crawler.sous_domaines:
            if sd.degre > 0 and sd.id_SD_Sous_domaine is not None:
                logger.debug(f"✓ {sd.url_SD} (degré {sd.degre}) -> Parent ID: {sd.id_SD_Sous_domaine}")
            elif sd.degre > 0:
                logger.warning(f"⚠ {sd.url_SD} (degré {sd.degre}) n'a pas de parent défini")
        
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