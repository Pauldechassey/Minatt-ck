from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserSchema, LoginRequest
from app.services.user_service import get_all_users, get_user_by_id, get_connection
from app.database import SessionLocal

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

@router.post("/auth/login", response_model=bool)
def login(json_data: LoginRequest, db: Session = Depends(get_db)) -> bool:
    return get_connection(json_data.dict(), db)
