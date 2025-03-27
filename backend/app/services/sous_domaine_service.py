from typing import List
from sqlalchemy.orm import Session
from app.models.sous_domaine import SousDomaine

def get_all_sous_domaines(db: Session):
    return db.query(SousDomaine).all()

def get_sous_domaine_by_id(sous_domaine_id: int, db: Session):
    return db.query(SousDomaine).filter(SousDomaine.id_SD == sous_domaine_id).first()

def get_sous_domaines_by_domaine(domaine_id: int, db: Session):
    return db.query(SousDomaine).filter(SousDomaine.id_domaine == domaine_id).all()



def get_all_child_urls_recursively(initial_url: str, db: Session) -> List[str]:
    initial_sous_domaine = db.query(SousDomaine).filter(
        SousDomaine.url_SD == initial_url
    ).first()

    if not initial_sous_domaine:
        raise ValueError(f"Aucun sous-domaine trouvé pour l'URL {initial_url}")
    
    urls_to_attack = [initial_url]
    
    #éviter les doublons
    processed_urls = {initial_url}
    queue = [initial_sous_domaine.id_SD]
    
    while queue:
        current_parent_id = queue.pop(0)
        
        child_sous_domaines = db.query(SousDomaine).filter(
            SousDomaine.id_domaine == current_parent_id
        ).all()
        
        for child_sous_domaine in child_sous_domaines:
            if child_sous_domaine.url_SD not in processed_urls:
                processed_urls.add(child_sous_domaine.url)
                urls_to_attack.append(child_sous_domaine.url)
                
                queue.append(child_sous_domaine.id_SD)
    
    return urls_to_attack
