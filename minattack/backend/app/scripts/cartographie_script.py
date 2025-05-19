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
    
    crawler = WebCrawler(base_url, id_audit=id_audit, id_domaine=id_domaine)
    
    crawler.crawl_bfs()
    
    logger.info(f"Crawling terminé, {len(crawler.sous_domaines)} sous-domaines trouvés")
    
    # Trier les sous-domaines par degré pour maintenir l'ordre BFS
    crawler.sous_domaines.sort(key=lambda sd: (sd.degre, sd.url_SD))
    
    nb_sd = 0
    nb_techs = 0
    tech_ids = {}  # Pour stocker les IDs des technologies après l'ajout en BDD
    
    parent_map = {}  # Pour stocker la correspondance index -> id_SD après le flush
    
    for i, sd in enumerate(crawler.sous_domaines):
        db.add(sd)
        db.flush()  # Flush pour obtenir l'ID généré
        parent_map[i] = sd.id_SD
        nb_sd += 1
        logger.debug(f"Sous-domaine ajouté: {sd.url_SD} (ID: {sd.id_SD}, degré: {sd.degre})")
    
    for i, sd in enumerate(crawler.sous_domaines):
        if i > 0:  # Ignorer la racine
            # Trouver l'URL parent et récupérer son ID de la BDD
            parent_url = None
            for parent_url, index in crawler.url_to_sd_id.items():
                if sd.id_SD_Sous_domaine == index:
                    parent_url = parent_url
                    break
            
            if parent_url in crawler.url_to_sd_id:
                parent_index = crawler.url_to_sd_id[parent_url]
                parent_id = parent_map.get(parent_index)
                if parent_id:
                    sd.id_SD_Sous_domaine = parent_id
                    db.merge(sd)
    
    # Ajouter les technologies à la base de données
    for i, tech in enumerate(crawler.technologies):
        db.add(tech)
        db.flush()
        tech_ids[i] = tech.id_techno
        nb_techs += 1
        logger.debug(f"Technologie ajoutée: {tech.nom_techno} v{tech.version_techno} (ID: {tech.id_techno})")
    
    # Ajouter les relations Utiliser
    for utiliser, tech_index in crawler.relations_utiliser:
        utiliser.id_techno = tech_ids.get(tech_index)
        if utiliser.id_techno:
            db.add(utiliser)
            db.flush()
            logger.debug(f"Relation ajoutée: Domaine {utiliser.id_domaine} utilise Techno {utiliser.id_techno}")
    
    db.commit()
    
    # Valider la réussite du processus
    return nb_sd == len(crawler.sous_domaines) and nb_techs == len(crawler.technologies)