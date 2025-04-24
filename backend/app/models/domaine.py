from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Domaine(Base):
    __tablename__ = "Domaine"

    id_domaine = Column(Integer, primary_key=True, autoincrement=True)
    url_domaine = Column(String, nullable=False)
    description_domaine = Column(Text)
