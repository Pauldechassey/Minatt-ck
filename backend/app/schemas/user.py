from pydantic import BaseModel


class UserSchema(BaseModel):
    id_user: int
    nom_user: str
    mdp_user: str
    role: int

    class Config:
        orm_mode = True


class LoginRequest(BaseModel):
    nom_user: str
    hashed_credentials: str