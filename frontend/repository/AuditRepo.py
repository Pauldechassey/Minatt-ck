import requests
import os
import dotenv

dotenv.load_dotenv()


class AuditRepo:
    def __init__(self):
        base_url = os.getenv("BASE_URL")
        port = os.getenv("PORT")
        if not base_url or not port:
            raise ValueError("AuditRepo: BASE_URL or PORT environment variables not set")
        self.__url = f"{base_url}:{port}/"

    def sendAuditUrl(self, audit_url: str):
        new_url = self.__url + "audit"
        data = {"audit_url": audit_url}
        try:
            response = requests.post(url=new_url, data=data, timeout=30)
            return response.status_code
        except requests.exceptions.Timeout:
            print("AuditRepo: request timed out")
        except requests.exceptions.RequestException as e:
            print(f"Error creating an audit: {e}")

