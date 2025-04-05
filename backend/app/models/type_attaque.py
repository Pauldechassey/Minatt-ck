from sqlalchemy import Column, Integer, String, Text
from backend.app.database import Base

class Type_attaque(Base):
    __tablename__ = "Type_attaque"

    id_Type = Column(Integer, primary_key=True, autoincrement=True)
    nom_type = Column(String, nullable=False)
    description_type = Column(Text, nullable=False)