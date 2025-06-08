from fastapi import APIRouter, Depends, HTTPException
from minattack.backend.app.database import SessionLocal
from sqlalchemy.orm import Session
import logging

from minattack.backend.app.globals import CURRENT_AUDIT
from minattack.backend.app.services.audit_service import get_audit_by_id
from minattack.backend.app.services.cartographie_service import (
    run_cartographie,
)

router = APIRouter(prefix="/cartographie", tags=["Cartographie"])
logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", summary="Cartographie", status_code=200)
def cartographie_all(
    id_audit: int = CURRENT_AUDIT,
    fuzzing: bool = False,
    wordlist_path: str = None,
    db: Session = Depends(get_db),
):
    audit = get_audit_by_id(id_audit, db)
    if not audit:
        raise HTTPException(
            status_code=404, detail=f"Audit avec ID {id_audit} non trouvé"
        )

    try:
        logger.info(
            f"Démarrage cartographie pour domaine ID: {audit.id_domaine}"
        )

        logger.info("=" * 66)
        logger.info(
            f"Paramètres reçus - fuzzing: {fuzzing}, wordlist path: '{wordlist_path}'"
        )
        logger.info("=" * 66)

        result = run_cartographie(
            audit=audit,
            db=db,
            fuzzing=fuzzing,
            wordlist_path=(
                wordlist_path
                if wordlist_path
                else "minattack/backend/wordlist/worlist_fuzzer.csv"
            ),
        )

        if isinstance(result, dict):
            nb_sous_domaines = result.get("sous_domaines_saved", 0)
            nb_urls_totales = result.get("total_urls_crawled", 0)
            nb_technologies = result.get("technologies_saved", 0)
            nb_erreurs = result.get("errors", 0)

            logger.info(
                f"Résultats: {nb_sous_domaines} sous-domaines, {nb_urls_totales} URLs, {nb_technologies} technologies"
            )

            # Réponse structurée
            return {
                "success": True,
                "message": "Cartographie effectuée avec succès",
                "resultats": {
                    "sous_domaines_sauvegardes": nb_sous_domaines,
                    "urls_totales_analysees": nb_urls_totales,
                    "technologies_detectees": nb_technologies,
                    "erreurs": nb_erreurs,
                },
                "details_complets": result,
            }
        else:
            logger.warning(f"Type de retour inattendu: {type(result)}")
            return {
                "success": True,
                "message": "Cartographie terminée",
                "result": str(result),
            }

    except Exception as e:
        logger.error(f"Erreur lors de la cartographie: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
