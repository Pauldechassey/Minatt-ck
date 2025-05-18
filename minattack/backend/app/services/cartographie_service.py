from sqlalchemy.orm import Session
import logging

from minattack.backend.app.models.audit import Audit
from minattack.backend.app.models.domaine import Domaine
from minattack.backend.app.scripts.cartographie_script import WebCrawler
from minattack.backend.app.services.domaine_service import get_domaine_by_id

logger = logging.getLogger(__name__)

def run_cartographie(audit : Audit,db: Session) -> int:
    domaine = db.query(Domaine).filter(Domaine.id_domaine == audit.id_domaine).first()
    if not domaine:
        raise Exception(f"Domaine avec ID {audit.id_domaine} non trouvé")
    
    base_url = domaine.url_domaine
    logger.info("debut crawling")
    crawler = WebCrawler(base_url, domaine)
    crawler.crawl(db)
    logger.info(crawler)
    return len(crawler.sous_domaines_crawler_map)