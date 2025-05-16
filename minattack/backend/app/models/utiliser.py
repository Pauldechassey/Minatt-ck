from sqlalchemy import Column, Integer, ForeignKey
from minattack.backend.app.database import Base


class Utiliser(Base):
    __tablename__ = "Utiliser"

    id_domaine = Column(Integer, ForeignKey("Domaine.id_domaine"), primary_key=True)
    id_techno = Column(Integer, ForeignKey("Technologie.id_techno"), primary_key=True)
