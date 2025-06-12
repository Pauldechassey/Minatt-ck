import requests
from minattack.shared.env import get_backend_host, get_backend_port

class AttaquesRepo:
    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super(AttaquesRepo, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.__url = f"{get_backend_host()}:{get_backend_port()}/attaque"

    def send_attacks(self, id_audit: int, attack_list: list[str], audit_state: int):
        """Lance des attaques normales via la route /attaque/"""
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

        if not self._validate_params(id_audit, attack_list):
            return None
                    
        endpoint = f"{self.__url}/"
        payload = {
            "id_audit": id_audit,
            "attaque_type": attack_list
        }
        
        print(f"[DEBUG] Launching normal attacks: {attack_list} on audit {id_audit}")
        return self._post(endpoint, payload)

    def send_attacks_cluster(self, id_audit: int, attack_list: list[str], audit_state: int):
        """Lance des attaques par cluster via la route /attaque/cluster"""
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

        # Validation des paramètres
        if not self._validate_params(id_audit, attack_list):
            return None
                    
        endpoint = f"{self.__url}/cluster"
        payload = {
            "id_audit": id_audit,
            "attaque_type": attack_list
        }
        
        print(f"[DEBUG] Launching cluster attacks: {attack_list} on audit {id_audit}")
        return self._post(endpoint, payload)

    def _validate_params(self, id_audit: int, attack_list: list[str]) -> bool:
        """Valide les paramètres communs aux différentes méthodes d'attaque"""
        if id_audit is None:
            print("[ERROR] sd_initial_id cannot be None")
            return False

        if not isinstance(id_audit, int):
            print(f"[ERROR] sd_initial_id must be an integer, got {type(id_audit)}")
            return False
                
        if id_audit <= 0:
            print(f"[ERROR] sd_initial_id must be positive, got {id_audit}")
            return False

        if not attack_list or not isinstance(attack_list, list):
            print(f"[ERROR] attack_list must be a non-empty list, got {attack_list}")
            return False
            
        return True

    def _post(self, endpoint: str, payload: dict, params: dict = None):
        try:
            print(f"[DEBUG] Attempting to send request to {endpoint}")
            print(f"[DEBUG] Payload: {payload}")
            print(f"[DEBUG] Params: {params}")
            
            response = requests.post(
                url=endpoint, 
                json=payload, 
                params=params
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

