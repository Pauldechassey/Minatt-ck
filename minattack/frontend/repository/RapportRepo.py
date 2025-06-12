import os
import requests
from minattack.shared.env import get_backend_host, get_backend_port


class RapportRepo:
    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super(RapportRepo, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.__url = f"{get_backend_host()}:{get_backend_port()}/rapport"

    def download_rapport(self, audit_id: int) -> tuple[bool, str | None]:
        """Récupère le rapport PDF pour affichage dans le navigateur"""
        try:
            response = requests.get(
                f"{self.__url}/download/{audit_id}", timeout=30
            )
            if response.status_code == 200:
                print("[SUCCESS] Rapport téléchargé")
                return True, response.json()["file_path"]
            print(
                f"[FAILED] Échec du téléchargement du rapport: {response.text}"
            )
            return False, None
        except Exception as e:
            print(f"[ERROR] {e}")
            return False, None

    def get_data_rapport(self, audit_id: int) -> tuple[bool, str]:
        """Télécharge le rapport PDF"""
        file_path = ""
        try:
            response = requests.get(
                f"{self.__url}/data/{audit_id}", timeout=30
            )
            if response.status_code == 200:
                pdf_data = response.content
                file_path = str(response.headers.get("X-File-Path"))
                with open(file_path, "wb") as f:
                    f.write(pdf_data)
                print(f"[SUCCESS] Rapport téléchargé: {file_path}")
                return True, file_path
            print(f"[FAILED] Échec du téléchargement: {response.text}")
            return False, file_path
        except Exception as e:
            os.remove(file_path)
            print(f"[ERROR] {e}")
            return False, file_path
