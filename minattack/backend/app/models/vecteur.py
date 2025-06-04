from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from minattack.backend.app.database import Base


class Vecteur(Base):
    __tablename__ = "Vecteur"

    id_vecteur = Column(Integer, primary_key=True, autoincrement=True)
    vecteur = Column(String, nullable=False)  # Stocké sous forme JSON ou CSV (ex: "0.1,0.2,0.3,...")
    cluster = Column(Integer, nullable=True)  # Cluster ID, peut être NULL si non assigné

    id_SD = Column(Integer, ForeignKey("Sous_domaine.id_SD"), nullable=False)
    sous_domaine = relationship("SousDomaine", back_populates="vecteur")
