class User:
    def __init__(self, name: str, password: str, role: str):
        self._name = name
        self._password = password
        self._role = role

    def getName(self) -> str:
        return self.__name

    def getRole(self) -> str:
        return self.__role

    def setName(self, name: str):
        self.__name = name

    def setRole(self, role: str):
        self.__role = role

    def __str__(self) -> str:
        return f"User(name={self._name}, role={self._role})"

    def __repr__(self) -> str:
        return f"User('{self._name}', '********', '{self._role}')"
