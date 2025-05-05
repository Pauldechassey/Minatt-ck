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
        endpoint = f"{self.__url}/recursive/list/"
        payload = {
            "SD_initial_id": sd_initial_id,
            "attaque_type": attack_list
        }
        return self._post(endpoint, payload)

    def send_attacks_single(self, sd_initial_id: int, attack_list: list[str], audit_state: int):
        # Validation de l'état de l'audit
        if audit_state != 1:
            if audit_state == 0:
                print("[ERROR] La cartographie n'a pas encore été effectuée")
                return None
            elif audit_state == 2:
                print("[ERROR] Une attaque a déjà été lancée sur cet audit")
                return None
            else:
                print(f"[ERROR] État d'audit invalide: {audit_state}")
                return None

        # Validation existante des paramètres
        if sd_initial_id is None:
            print("[ERROR] sd_initial_id cannot be None")
            return None

        if not isinstance(sd_initial_id, int):
            print(f"[ERROR] sd_initial_id must be an integer, got {type(sd_initial_id)}")
            return None
                
        if sd_initial_id <= 0:
            print(f"[ERROR] sd_initial_id must be positive, got {sd_initial_id}")
            return None

        if not attack_list or not isinstance(attack_list, list):
            print(f"[ERROR] attack_list must be a non-empty list, got {attack_list}")
            return None
                    
        endpoint = f"{self.__url}/single/list/"
        payload = {
            "attaque_type": attack_list
        }
        params = {
            "SD_initial_id": sd_initial_id
        }
        
        print(f"[DEBUG] Launching attacks: {attack_list} on SD {sd_initial_id}")
        return self._post(endpoint, payload, params)

    def send_attacks_all(self, sd_initial_id: int):
        endpoint = f"{self.__url}/all/"
        payload = {
            "SD_initial_id": sd_initial_id
        }
        return self._post(endpoint, payload)

    def _post(self, endpoint: str, payload: dict, params: dict = None):
        try:
            print(f"[DEBUG] Attempting to send request to {endpoint}")
            print(f"[DEBUG] Payload: {payload}")
            print(f"[DEBUG] Params: {params}")
            
            response = requests.post(
                url=endpoint, 
                json=payload, 
                params=params,
                timeout=30
            )
            print(f"[DEBUG] Response status: {response.status_code}")
            print(f"[DEBUG] Response content: {response.text}")
            
            if response.status_code == 200:
                print(f"[SUCCESS] Attack request successful")
                return response.json()
            else:
                print(f"[FAILED] Attack request failed: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Request failed: {str(e)}")
            return None

