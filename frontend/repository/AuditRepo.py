import requests
import os
import dotenv

dotenv.load_dotenv()

class AuditRepo:
    def __init__(self):
        base_url = os.getenv("BASE_URL")
        port = os.getenv("PORT")
        self.__url = f"{base_url}:{port}/audit"

    def sendAuditUrl(self, audit_url: str):
        data = {"audit_url": audit_url}
        try: 
            response = requests.post(url=BASE_URL, json=data, timeout=100)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending audit URL: {e}")
            return None