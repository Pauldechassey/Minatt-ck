from sqlalchemy import Column, Integer, String
from minattack.backend.app.database import Base

class Technologie(Base):
    __tablename__ = "Technologie"

    id_techno = Column(Integer, primary_key=True, autoincrement=True)
    nom_techno = Column(String, nullable=False)
    version_techno = Column(String, nullable=False)