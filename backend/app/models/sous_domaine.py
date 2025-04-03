from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class SousDomaine(Base):
    __tablename__ = "Sous_domaine"

    id_SD = Column(Integer, primary_key=True, autoincrement=True)
    url_SD = Column(String(50), nullable=True)
    description_SD = Column(String(255), nullable=True)
    id_domaine = Column(Integer, nullable=False)

    attaques = relationship("Attaque", back_populates="sous_domaine")