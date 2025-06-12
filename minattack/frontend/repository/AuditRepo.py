from typing import Any
import requests
from minattack.shared.env import get_backend_host, get_backend_port


class AuditRepo:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuditRepo, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.__url = f"{get_backend_host()}:{get_backend_port()}/"

    def getAllAudits(self) -> bool:
        new_url = self.__url + "audits/all"
        try:
            response = requests.get(url=new_url, timeout=30)
            if response.status_code == 200:
                print("AuditRepo [SUCCESS]: audits fetching successful")
                return True
            print("AuditRepo [FAILED]: audit fetching failed")
            return False
        except requests.exceptions.Timeout:
            print("AuditRepo [TIMEOUT]: request timed out")
            return False
        except requests.exceptions.RequestException as e:
            print(f"AuditRepo [ERROR]: {e}")
            return False

    def getAuditsDomaines(self) -> tuple[bool, Any]:
        new_url = self.__url + "audits/menu_list"
        try:
            response = requests.get(url=new_url, timeout=30)
            if response.status_code == 200:
                print("AuditRepo [SUCCESS]: audits fetching successful")
                return True, response.json()
            print("AuditRepo [FAILED]: audit fetching failed")
            return False, None
        except requests.exceptions.Timeout:
            print("AuditRepo [TIMEOUT]: request timed out")
            return False, None
        except requests.exceptions.RequestException as e:
            print(f"AuditRepo [ERROR]: {e}")
            return False, None

    def createAudit(self, url_domaine: str) -> tuple[bool, Any]:
        new_url = self.__url + "audits/new"
        data = {"url_domaine": url_domaine}
        try:
            response = requests.post(url=new_url, json=data, timeout=30)
            if response.status_code == 201:
                print("AuditRepo [SUCCESS]: audit creation successful")
                # print("------------")
                # print(f"AUDIT REPO : {response.json()["id"]}")
                # print("------------")
                return True, response.json()["id"]
            print("AuditRepo [FAILED]: audit creation failed")
            return False, None
        except requests.exceptions.Timeout:
            print("AuditRepo [TIMEOUT]: request timed out")
            return False, None
        except requests.exceptions.RequestException as e:
            print(f"AuditRepo [ERROR]: {e}")
            return False, None

    def updateAuditState(self, id: int, state: int) -> bool:
        new_url = self.__url + "audits/update_state"
        data = {"id_audit": id, "new_state": state}
        try:
            response = requests.post(url=new_url, json=data, timeout=30)
            if response.status_code == 200:
                print("AuditRepo [SUCCESS]: audit update successful")
                return True
            print("AuditRepo [FAILED]: audit update failed")
            return False
        except requests.exceptions.Timeout:
            print("AuditRepo [TIMEOUT]: request timed out")
            return False
        except requests.exceptions.RequestException as e:
            print(f"AuditRepo [ERROR]: {e}")
            return False
