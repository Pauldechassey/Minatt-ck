import os
import sys
from dotenv import load_dotenv

def get_app_root():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

def get_path(relative_path: str) -> str:
    return os.path.join(get_app_root(), relative_path)

def load_env():
    dotenv_path = get_path(".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path=dotenv_path)
    else:
        print(f"[WARNING] .env not found at: {dotenv_path}")

def get_env(default="dev") -> str:
    return os.getenv("ENV", default)