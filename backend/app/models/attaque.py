from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Attaque(Base):
    __tablename__ = "Attaque"

    id_attaque = Column(Integer, primary_key=True, autoincrement=True)
    payload = Column(String, nullable=False)
    date_attaque = Column(DateTime, nullable=False)
    resultat = Column(Integer, nullable=False)  # 0 = False, 1 = True
    id_SD = Column(Integer, ForeignKey("Sous_domaine.id_SD"), nullable=False)
    id_Type = Column(Integer, ForeignKey("Type.id_Type"), nullable=False)

    sous_domaine = relationship("SousDomaine", backref="attaques")
    attaque_type = relationship("Type", backref="attaques")
