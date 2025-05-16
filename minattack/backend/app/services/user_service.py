from sqlalchemy.orm import Session
from minattack.backend.app.models.user import User


def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()


def get_user_by_id(user_id: int, db: Session) -> User | None:
    return db.query(User).filter(User.id_user == user_id).first()


def get_mdp_by_nom(nom_user: str, db: Session) -> str | None:
    result = db.query(User.mdp_user).filter(User.nom_user == nom_user).first()
    return result[0] if result else None


def connect_user(data: dict, db: Session) -> User | None:
    nom_user = data.get("nom_user")
    hashed_credentials = data.get("hashed_credentials")

    if not nom_user or not hashed_credentials:
        return None

    user = db.query(User).filter(User.nom_user == nom_user).first()

    if user and hashed_credentials == user.mdp_user:
        return user

    return None


def unconnect_user() -> None:
    return None
