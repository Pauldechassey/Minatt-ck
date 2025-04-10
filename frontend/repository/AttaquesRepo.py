import requests
import os
import dotenv

dotenv.load_dotenv()

class AttaquesRepo:
    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super(AttaquesRepo, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        base_url = os.getenv("BASE_URL")
        port = os.getenv("PORT")
        if not base_url or not port:
            raise ValueError("AttaquesRepo: BASE_URL or PORT not set in .env")
        self.base_url = f"{base_url}:{port}/attaque"

    def send_attacks_recursive(self, sd_initial_id: int, attack_list: list[str]):
        url = f"{self.base_url}/recursive/list/"
        params = {
            "SD_initial_id": sd_initial_id,
            "attaque_type": attack_list
        }
        try:
            response = requests.post(url=url, params=params, timeout=30)
            if response.status_code == 200:
                print("[SUCCESS] Attaques récursives envoyées")
                return response.json()
            else:
                print(f"[FAILED] {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Erreur lors de l'envoi des attaques : {e}")
            return None

    def send_attacks_single(self, sd_initial_id: int, attack_list: list[str]):
        url = f"{self.base_url}/single/list/"
        params = {
            "SD_initial_id": sd_initial_id,
            "attaque_type": attack_list
        }
        try:
            response = requests.post(url=url, params=params, timeout=30)
            if response.status_code == 200:
                print("[SUCCESS] Attaques uniques envoyées")
                return response.json()
            else:
                print(f"[FAILED] {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Erreur lors de l'envoi des attaques : {e}")
            return None
