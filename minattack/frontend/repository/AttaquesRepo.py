import os
import requests
from minattack.shared.env import get_backend_host, get_backend_port

class AttaquesRepo:
    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super(AttaquesRepo, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.__url = f"{get_backend_host()}:{get_backend_port()}/attaque"

    def send_attacks_recursive(self, sd_initial_id: int, attack_list: list[str]):
        url = f"{self.__url}/recursive/list/"
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
        url = f"{self.__url}/single/list/"
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
