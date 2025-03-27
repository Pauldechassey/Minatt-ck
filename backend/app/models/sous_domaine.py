from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class SousDomaine(Base):
    __tablename__ = "Sous_domaine"

    id_SD = Column(Integer, primary_key=True, autoincrement=True)
    url_SD = Column(String, nullable=False)
    description_SD = Column(Text, nullable=False)
    degre = Column(Integer, nullable=False)
    id_domaine = Column(Integer, ForeignKey("Domaine.id_domaine"), nullable=False)
    id_SD_Sous_domaine = Column(Integer, ForeignKey("Sous_domaine.id_SD"))

    domaine = relationship("Domaine", backref="sous_domaines")
    parent_sous_domaine = relationship("SousDomaine", remote_side=[id_SD], backref="sub_sous_domaines")