import os
import requests
from dotenv import load_dotenv

load_dotenv()


class UserRepo:
    def __init__(self):
        base_url = os.getenv("BASE_URL")
        port = os.getenv("PORT")
        if not base_url or not port:
            raise ValueError("UserRepo: BASE_URL or PORT environment variables not set")
        self.__url = f"{base_url}:{port}/"

    def login(self, nom_user: str, mdp_user: str):
        new_url = self.__url + "auth/login"
        data = {"api_name": nom_user, "api_password": mdp_user}
        try:
            response = requests.post(url=new_url, data=data, timeout=30)
            return response.status_code
        except requests.exceptions.Timeout:
            print("UserRepo: request timed out")
        except requests.exceptions.RequestException as e:
            print(f"Errors sending credentials: {e}")
