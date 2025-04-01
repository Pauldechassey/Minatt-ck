import os
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "../db")
DB_FILE = os.path.join(DB_DIR, "minattack.sqlite")

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE}"

#engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base = declarative_base()


def init_db():
    print("Initializing database...")
    print(f"BASE_DIR : {BASE_DIR}")
    print(f"DB_DIR : {DB_DIR}")
    print(f"DB_file : {DB_FILE}")
    if not os.path.exists(DB_FILE):

        print(f"🔧 Creating database at {DB_FILE}...")
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Load schema from `init.sql`
        sql_file_path = os.path.join(BASE_DIR, "../app/database/init.sql")
        print(f"sql_file_path : {sql_file_path}")
        if os.path.exists(sql_file_path):
            with open(sql_file_path, "r") as f:
                sql_script = f.read()
                cursor.executescript(sql_script)  # ✅ Runs SQL initialization script
        else:
            print("⚠️ Warning: init.sql not found. Skipping SQL script execution.")

        conn.commit()
        conn.close()
        print("✅ Database initialized successfully!")
    else:
        print(f"✅ Database already exists at {DB_FILE}. No initialization needed.")


# ✅ Run `init_db()` when this script is executed
if __name__ == "__main__":
    init_db()