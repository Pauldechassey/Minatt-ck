import requests
from utils.env import get_backend_host, get_backend_port



class UserRepo:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserRepo, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.__url = f"{get_backend_host()}:{get_backend_port()}/"

    def login(self, nom_user: str, hashed_credentials: str):
        new_url = self.__url + "users/auth/login"
        data = {"nom_user": nom_user, "hashed_credentials": hashed_credentials}
        try:
            response = requests.post(url=new_url, json=data, timeout=30)
            if response.status_code == 200:
                print("UserRepo [SUCCESS]: login successful")
                return True
            print("UserRepo [FAILED]: login failed")
            return False
        except requests.exceptions.Timeout:
            print(f"UserRepo [TIMEOUT]: login request timed out")
        except requests.exceptions.RequestException as e:
            print(f"UserRepo [ERROR]: {e}")
        return False

    def logout(self):
        new_url = self.__url + "users/auth/logout"
        try:
            response = requests.post(url=new_url, timeout=30)
            if response.status_code == 200:
                print("UserRepo [SUCCESS]: logout successful")
                return True
            print("UserRepo [FAILED]: logout failed")
            return False
        except requests.exceptions.Timeout:
            print("UserRepo [TIMEOUT]: logout request timed out")
        except requests.exceptions.RequestException as e:
            print(f"UserRepo [ERROR]: {e}")
        return False
