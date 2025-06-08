import os
import requests
from minattack.shared.env import get_backend_host, get_backend_port


class CartoRepo:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CartoRepo, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.__url = f"{get_backend_host()}:{get_backend_port()}/"

    def runCarto(self, id_audit: int):
        new_url = self.__url + f"cartographie/{id_audit}"  # A COMPLETER QUAND LA ROUTE DU BACK EST LA
        try:
            response = requests.post(url=new_url, timeout=30)
            if response.status_code == 200:
                print("AuditRepo [SUCCESS]: lancement de la cartographie")
                return True
            print("AuditRepo [FAILED]: echec de lancement de la cartographie")
            return False
        except requests.exceptions.Timeout:
            print("AuditRepo [TIMEOUT]: request timed out")
        except requests.exceptions.RequestException as e:
            print(f"AuditRepo [ERROR]: {e}")
        return False
