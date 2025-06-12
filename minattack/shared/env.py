import os
import sys
from pathlib import Path
from platformdirs import user_data_dir
from dotenv import load_dotenv

LOCAL_DB_PATH = "minattack/backend/db/minattack.sqlite"
LOCAL_RAPPORT_PATH = "Rapports"


def is_frozen() -> bool:
    return getattr(sys, "frozen", False)


def get_app_root() -> str:
    if is_frozen():
        return sys._MEIPASS
    else:
        return str(Path(__file__).resolve().parents[2])


def get_path(relative_path: str) -> str:
    return str(Path(get_app_root()) / relative_path)


def load_env(override: bool = False):
    dotenv_path = get_path(".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path=dotenv_path, override=override)
    else:
        print(f"[WARNING] .env not found at: {dotenv_path}")


def get_env(default: str = "dev") -> str:
    return os.getenv("ENV", default)


def get_backend_port(default: int = 8000) -> str:
    return os.getenv("BACKEND_PORT", str(default))


def get_backend_host(default: str = "http://127.0.0.1") -> str:
    return os.getenv("HOST", default)


def set_dynamic_backend_port(port: int):
    os.environ["BACKEND_PORT"] = str(port)
    load_env()


def get_database_paths() -> str:
    if is_frozen():
        return str(Path(user_data_dir()) / "MinAttack" / "minattack.sqlite")
    else:
        return get_path(LOCAL_DB_PATH)


def get_report_dir_path() -> str:
    if is_frozen():
        rapport_path = str(Path(user_data_dir()) / "MinAttack" / "Rapports")
    else:
        rapport_path = get_path(LOCAL_RAPPORT_PATH)
    if not os.path.exists(rapport_path):
            os.makedirs(rapport_path)
    return rapport_path
