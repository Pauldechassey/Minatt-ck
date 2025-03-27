from PySide6.QtWidgets import QWidget, QStackedWidget, QMessageBox, QLineEdit
from frontend.repository.UserRepo import UserRepo
from ui.ui_login import Ui_Login
from hashlib import sha256


class LoginWindow(QWidget, Ui_Login):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Login()
        self.ui.setupUi(self)

        self.userRepo = UserRepo()

        # Connexion du bouton login
        self.ui.buttonLogin.clicked.connect(self.check_credentials)

        # Connexion de la touche Entrée
        self.ui.lineEditPasswordLogin.returnPressed.connect(self.check_credentials)  # Appuie sur "Entrée" pour se connecter

    def check_credentials(self):
        user = self.ui.lineEditUsernameLogin.text()
        password = self.ui.lineEditPasswordLogin.text()
        hashed_credentials = sha256((user + password).encode())
        response = self.userRepo.login(user, password)
        if response == 200:
            parent = self.parentWidget()
            if isinstance(parent, QStackedWidget):
                parent.setCurrentIndex(1)
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials")
