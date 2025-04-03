import os
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "../db")
DB_FILE = os.path.join(DB_DIR, "minattack.sqlite")

# SQLAlchemy connection string
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE}"

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base
Base = declarative_base()


def init_db(force=False):
    """Initialize the database using init.sql

    Args:
        force (bool): If True, will reinitialize the database even if it already exists
    """
    print("Initializing database...")
    print(f"BASE_DIR : {BASE_DIR}")
    print(f"DB_DIR : {DB_DIR}")
    print(f"DB_file : {DB_FILE}")

    # Create DB directory if it doesn't exist
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)

    # Check if database should be initialized
    if not os.path.exists(DB_FILE) or force:
        if os.path.exists(DB_FILE) and force:
            print(f"Reinitializing database at {DB_FILE}...")
            os.remove(DB_FILE)
        else:
            print(f"Creating database at {DB_FILE}...")

        # Create DB connection
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Load schema from `init.sql`
        sql_file_path = os.path.join(BASE_DIR, "../app/database/init.sql")
        print(f"sql_file_path : {sql_file_path}")

        if os.path.exists(sql_file_path):
            with open(sql_file_path, "r") as f:
                sql_script = f.read()
                cursor.executescript(sql_script)  # Runs SQL initialization script
        else:
            print("Warning: init.sql not found. Skipping SQL script execution.")

        conn.commit()
        conn.close()
        print("Database initialized successfully!")
    else:
        print(f"Database already exists at {DB_FILE}. No initialization needed.")
        print("   Use init_db(force=True) to reinitialize the database.")


# Database session context manager
def get_db():
    """Get a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Run `init_db()` when this script is executed directly
if __name__ == "__main__":
    init_db()

