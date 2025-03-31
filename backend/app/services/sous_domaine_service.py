from typing import List
from sqlalchemy import select, union_all
from sqlalchemy.orm import Session
from app.models.sous_domaine import SousDomaine

def get_all_sous_domaines(db: Session):
    return db.query(SousDomaine).all()

def get_sous_domaine_by_id(sous_domaine_id: int, db: Session):
    return db.query(SousDomaine).filter(SousDomaine.id_SD == sous_domaine_id).first()

def get_sous_domaines_by_domaine(domaine_id: int, db: Session):
    return db.query(SousDomaine).filter(SousDomaine.id_domaine == domaine_id).all()


def get_all_child_urls_recursively(initial_url: str, db: Session) -> List[str]:
    # Vérifier que le sous-domaine initial existe
    initial_sous_domaine = db.query(SousDomaine).filter(
        SousDomaine.url_SD == initial_url
    ).first()
    
    if not initial_sous_domaine:
        raise ValueError(f"Aucun sous-domaine trouvé pour l'URL {initial_url}")
    
    # Utiliser une CTE récursive pour obtenir tous les sous-domaines d'un seul coup
    with db.connection() as conn:
        # Définir la requête CTE récursive
        cte_stmt = (
            select(SousDomaine.id_SD, SousDomaine.url_SD)
            .where(SousDomaine.id_SD == initial_sous_domaine.id_SD)
            .cte(recursive=True)
        )
        
        # Partie récursive de la CTE
        included_sub_domains = (
            select(SousDomaine.id_SD, SousDomaine.url_SD)
            .join(cte_stmt, SousDomaine.id_domaine == cte_stmt.c.id_SD)
        )
        
        cte_stmt = cte_stmt.union_all(included_sub_domains)
        
        results = conn.execute(select(cte_stmt.c.url_SD)).fetchall()
    
    urls_to_attack = [row[0] for row in results]
    
    return urls_to_attack