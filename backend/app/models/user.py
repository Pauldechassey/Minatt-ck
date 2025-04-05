from sqlalchemy import Column, Integer, String
from backend.app.database import Base

class User(Base):
    __tablename__ = "User"

    id_user = Column(Integer, primary_key=True, autoincrement=True)
    nom_user = Column(String, nullable=False)
    mdp_user = Column(String, nullable=False)
    role = Column(Integer, nullable=False)