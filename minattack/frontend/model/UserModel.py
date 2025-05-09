class User:
    def __init__(self, id: int, name: str, role: str):
        self.id = id
        self.name = name
        self.role = role

    def __str__(self) -> str:
        return f"User(name={self.name}, role={self.role})"

    def __repr__(self) -> str:
        return f"User('{self.name}', '********', '{self.role}')"
