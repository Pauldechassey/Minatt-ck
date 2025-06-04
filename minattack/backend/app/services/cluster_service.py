import json
from fastapi import Depends
from requests import Session
from init_vector_script import InitVector
from minattack.backend.app.database.database import SessionLocal
from minattack.backend.app.globals import CURRENT_AUDIT
from minattack.backend.app.models.audit import Audit
from minattack.backend.app.models.domaine import Domaine
from minattack.backend.app.models.sous_domaine import SousDomaine
from minattack.backend.app.models.vecteur import Vecteur
from minattack.backend.app.services.embedder_service import Embedder
from minattack.backend.app.scripts.classification_DBSCAN_script import classification_DBSCAN



def cluster(db: Session):
    try:
        ids, vectors = get_vectors_from_db(db=db, audit_id=CURRENT_AUDIT)

        # Embedding
        embedder = Embedder(vectors)
        embedded_vectors = [embedder.embed(v) for v in vectors]

        # Clustering
        labels = classification_DBSCAN(embedded_vectors) 

        for id_sd, cluster_id in zip(ids, labels):
            vecteur = db.query(Vecteur).filter_by(id_SD=id_sd).first()
            if vecteur:
                vecteur.cluster = int(cluster_id)
        db.commit()

    except Exception as e:
        print(f"Error during clustering (w/ DBSCAN): {e}")    





def get_vectors_from_db(db: Session, audit_id = CURRENT_AUDIT):
    """
    Récupère tous les vecteurs de la base de données, associé à l'audit.
    """
    liste_sous_domaines = db.query(SousDomaine).join(Domaine).join(Audit).filter(Audit.id_audit == audit_id).all()
    
    vecteurs = (
        db.query(Vecteur)
        .filter(Vecteur.id_SD.in_([sd.id_SD for sd in liste_sous_domaines]))
        .all()
    )
    ids = [v.id_SD for v in vecteurs]
    vectors = [json.loads(v.vecteur) for v in vecteurs]

    return ids, vectors