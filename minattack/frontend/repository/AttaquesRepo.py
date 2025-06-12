import requests
from minattack.shared.env import get_backend_host, get_backend_port


class AttaquesRepo:
    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super(AttaquesRepo, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.__url = f"{get_backend_host()}:{get_backend_port()}/attaque"

    def send_attacks(self, id_audit: int, attack_list: list[str]):
        """Lance des attaques normales via la route /attaque/"""
        if not self._validate_params(id_audit, attack_list):
            return None

        endpoint = f"{self.__url}/"
        payload = {"attaque_type": attack_list}
        params = {"id_audit": id_audit}
        return self._post(endpoint, payload, params)

    def send_attacks_cluster(self, id_audit: int, attack_list: list[str]):
        """Lance des attaques par cluster via la route /attaque/cluster"""
        if not self._validate_params(id_audit, attack_list):
            return None
        endpoint = f"{self.__url}/cluster"
        payload = {"attaque_type": attack_list}
        params = {"id_audit": id_audit}
        return self._post(endpoint, payload, params)

    def _validate_params(self, id_audit: int, attack_list: list[str]) -> bool:
        """Valide les paramètres communs aux différentes méthodes d'attaque"""
        if id_audit <= 0:
            return False

        if not attack_list or not isinstance(attack_list, list):
            return False

        return True

    def _post(self, endpoint: str, payload: dict, params: dict = {}):
        try:
            response = requests.post(url=endpoint, json=payload, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                return None

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Request failed: {str(e)}")
            return None
