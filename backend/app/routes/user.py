from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserSchema, LoginRequest
from app.services.user_service import get_all_users, get_user_by_id, connect_user, unconnect_user
from app.database import SessionLocal
import app.globals as globals

router = APIRouter(prefix="/users", tags=["Users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[UserSchema])
def read_users(db: Session = Depends(get_db)) -> list[UserSchema]:
    return get_all_users(db)


@router.get("/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)) -> UserSchema:
    user = get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/auth/login", status_code=200)
def login(json_data: LoginRequest, db: Session = Depends(get_db)):
    globals.CONNECTED_USER = connect_user(json_data.model_dump(), db)
    if globals.CONNECTED_USER is not None: 
        return {"message": "Connexion réussie"}
    else:   
        raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect")
        
@router.post("/auth/logout", status_code=200)
def logout():
    globals.CONNECTED_USER = unconnect_user()
    if globals.CONNECTED_USER is not None: 
        raise HTTPException(status_code=401, detail="Déconnexion avortée")
    else:   
        return {"message": "Déconnexion réussie"}        
        