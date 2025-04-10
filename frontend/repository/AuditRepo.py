import requests
import os
import dotenv

dotenv.load_dotenv()


class AuditRepo:
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuditRepo, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        base_url = os.getenv("BASE_URL")
        port = os.getenv("PORT")
        if not base_url or not port:
            raise ValueError("AuditRepo: BASE_URL or PORT environment variables not set")
        self.__url = f"{base_url}:{port}/"

    def createAudit(self, url_domaine: str):
        new_url = self.__url + "audits/new"
        data = {"url_domaine": url_domaine}
        try:
            response = requests.post(url=new_url, json=data, timeout=30)
            if response.status_code == 200:
                print("AuditRepo [SUCCESS]: audit creation successful")
                return True
            print("AuditRepo [FAILED]: audit creation failed")
            return False
        except requests.exceptions.Timeout:
            print("AuditRepo [TIMEOUT]: request timed out")
        except requests.exceptions.RequestException as e:
            print(f"AuditRepo [ERROR]: {e}")
        return False
