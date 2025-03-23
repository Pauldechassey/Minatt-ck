from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Audit(Base):
    __tablename__ = "Audit"

    id_audit = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False)
    etat = Column(Integer, nullable=False)  # 0 = False, 1 = True
    path_rapport = Column(String)
    id_user = Column(Integer, ForeignKey("User.id_user"), nullable=False)
    id_domaine = Column(Integer, ForeignKey("Domaine.id_domaine"), nullable=False)

    user = relationship("User", backref="audits")
    domaine = relationship("Domaine", backref="audits")