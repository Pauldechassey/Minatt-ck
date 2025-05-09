from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from minattack.backend.app.database import Base

class Faille(Base):
    __tablename__ = "Faille"

    id_faille = Column(Integer, primary_key=True, autoincrement=True)
    gravite = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    balise = Column(Text, nullable=False)
    id_attaque = Column(Integer, ForeignKey("Attaque.id_attaque"), unique=True, nullable=False)

    attaque = relationship("Attaque", backref="faille")