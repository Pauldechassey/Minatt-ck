import requests


class UserRepo:
    def __init__(self, port=5000):
        self.__port = port
        self.__url = f"http://localhost{self.__port}/"

    def sendCredentials(self, name: str, password):
        data = {"api_name": name, "api_password": password}
        try:
            response = requests.post(url=self.__url, data=data, timeout=100)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Errors sending credentials: {e}")
            pass
