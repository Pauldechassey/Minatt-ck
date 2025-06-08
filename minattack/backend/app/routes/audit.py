# from fastapi import Body, Query
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from minattack.backend.app.schemas.audit import (
    AuditSchema,
    AuditStateUpdateSchema,
    UrlRequest,
)
from minattack.backend.app.schemas.audit_domaine import AuditDomaineSchema
from minattack.backend.app.services.audit_service import (
    create_new_audit,
    get_all_audits,
    get_audit_by_id,
    get_audits_and_domaines,
    update_audit_state,
)
from minattack.backend.app.database import SessionLocal

router = APIRouter(prefix="/audits", tags=["Audits"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/all", response_model=list[AuditSchema])
def read_audits(db: Session = Depends(get_db)):
    return get_all_audits(db)


@router.get("/menu_list", response_model=list[AuditDomaineSchema])
def read_audits_domaines(db: Session = Depends(get_db)):
    return get_audits_and_domaines(db)


@router.get("/{audit_id}", response_model=AuditSchema)
def read_audit(audit_id: int, db: Session = Depends(get_db)):
    audit = get_audit_by_id(audit_id, db)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    return audit


@router.post("/new", status_code=201)
def new_audit(url: UrlRequest, db: Session = Depends(get_db)):
    try:
        if (result := create_new_audit(url.url_domaine, db))[0]:
            return {"id": result[1]}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la création de l'audit: {str(e)}",
        )


@router.post("/update_state", status_code=status.HTTP_200_OK)
def change_audit_state(
    json_data: AuditStateUpdateSchema, db: Session = Depends(get_db)
):
    id_audit = json_data.id_audit
    new_state = json_data.new_state
    try:
        if id_audit is None or new_state is None:
            raise HTTPException(
                status_code=400,
                detail="Erreur :'id et le nouvel état ne peuvent pas être nuls",
            )
        elif id_audit < 0:
            raise HTTPException(
                status_code=400,
                detail="Erreur : l'id ne peut pas être négatif",
            )
        elif new_state < 1 or new_state > 3:
            raise HTTPException(
                status_code=400,
                detail="Erreur : l'état à appliquer ne peut pas être < 1 et > 3",
            )
        else:
            update_audit_state(id_audit, new_state, db)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la mise à jour de l'état: {str(e)}",
        )


# @router.put("/{audit_id}/state", status_code=200)
# def update_audit_state(
#     audit_id: int, new_state: int, db: Session = Depends(get_db)
# ):
#     try:
#         if new_state not in [0, 1, 2]:
#             raise HTTPException(status_code=400, detail="État invalide")
#         audit = get_audit_by_id(audit_id, db)
#         if not audit:
#             raise HTTPException(status_code=404, detail="Audit non trouvé")
#         if new_state <= audit.etat:
#             raise HTTPException(
#                 status_code=400, detail="Transition d'état invalide"
#             )
#         audit.etat = new_state
#         db.commit()
#         return {"message": f"État de l'audit mis à jour: {new_state}"}
#     except HTTPException as http_exc:
#         raise http_exc
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Erreur lors de la mise à jour de l'état: {str(e)}",
#         )
