import requests
from minattack.shared.env import get_backend_host, get_backend_port


class RapportRepo:
    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super(RapportRepo, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.__url = f"{get_backend_host()}:{get_backend_port()}/rapport"

    def view_rapport(self, audit_id: int) -> bytes:
        """Récupère le rapport PDF pour affichage dans le navigateur"""
        try:
            response = requests.get(
                f"{self.__url}/{audit_id}",
                timeout=30
            )
            if response.status_code == 200:
                print(f"[SUCCESS] Rapport généré pour l'audit {audit_id}")
                return response.content
            print(f"[FAILED] Échec de génération du rapport: {response.text}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] {e}")
            return None

    def download_rapport(self, audit_id: int, save_path: str) -> bool:
        """Télécharge le rapport PDF"""
        try:
            response = requests.get(
                f"{self.__url}/download/{audit_id}",
                timeout=30
            )
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                print(f"[SUCCESS] Rapport téléchargé: {save_path}")
                return True
            print(f"[FAILED] Échec du téléchargement: {response.text}")
            return False
        except Exception as e:
            print(f"[ERROR] {e}")
            return False