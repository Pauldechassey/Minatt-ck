import os
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.utils.env import get_path, get_env


DB_FILE = get_path("backend/db/minattack.sqlite")
SCHEMA_SQL_PATH = get_path("backend/app/database/schema.sql")
INIT_SQL_PATH = get_path("backend/app/database/init.sql")
DUMP_SQL_PATH = get_path("backend/app/database/data_dump.sql")

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE}"

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
    print(f"DB file : {DB_FILE}")

    # Create DB directory if it doesn't exist
    db_dir = os.path.dirname(DB_FILE)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

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

        print(f"Loading SQL from: {SCHEMA_SQL_PATH} and {INIT_SQL_PATH}")


        if os.path.exists(SCHEMA_SQL_PATH) and os.path.exists(INIT_SQL_PATH):
            with open(SCHEMA_SQL_PATH, "r") as f:
                sql_schema_script = f.read()
                cursor.executescript(sql_schema_script)
            with open(INIT_SQL_PATH, "r") as f:
                init_sql_script = f.read()
                cursor.executescript(init_sql_script)
            if get_env("dev")=="dev" and os.path.exists(DUMP_SQL_PATH):
                with open(DUMP_SQL_PATH, "r") as f:
                    sql_dump_script = f.read()
                    cursor.executescript(sql_dump_script)
        else:
            print("Warning: schema.sql and init.sql not found. Skipping SQL script execution.")

        conn.commit()
        conn.close()
        print("Database initialized successfully!")
    else:
        print(f"Database already exists at {DB_FILE}. No initialization needed.")


if __name__ == "__main__":
    init_db()