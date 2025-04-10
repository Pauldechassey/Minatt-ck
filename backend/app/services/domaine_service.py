from sqlalchemy.orm import Session
from backend.app.models.domaine import Domaine

def get_all_domaines(db: Session):
    return db.query(Domaine).all()

def get_domaine_by_id(domaine_id: int, db: Session):
    return db.query(Domaine).filter(Domaine.id_domaine == domaine_id).first()

def create_empty_domaine(url : str, db: Session):
    new_domaine = Domaine(url_domaine = url, description_domaine="")
    db.add(new_domaine)
    db.commit()
    db.refresh(new_domaine)
    return new_domaine.id_domaine