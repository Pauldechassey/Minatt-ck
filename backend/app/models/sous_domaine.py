from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship

class SousDomaine(Base):
    __tablename__ = "Sous_domaine"

    id_SD = Column(Integer, primary_key=True, index=True)
    url_SD = Column(String(50), nullable=True)
    description_SD = Column(String(255), nullable=True)
    id_domaine = Column(Integer, nullable=False)
