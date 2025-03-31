from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Définition du chemin vers la base de données
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "../db")
DB_FILE = os.path.join(DB_DIR, "minattack.sqlite")

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE}"

# Création du moteur SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Création d'une session locale
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour SQLAlchemy
Base = declarative_base()
