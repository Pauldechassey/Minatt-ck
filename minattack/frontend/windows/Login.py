from PySide6.QtWidgets import QWidget, QStackedWidget, QMessageBox
from minattack.frontend.ui.ui_login import Ui_Login
from hashlib import sha256


class LoginWindow(QWidget, Ui_Login):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        self.main_window = main_window

        # Connexion du bouton login
        self.ui.buttonLogin.clicked.connect(self.check_credentials)

        # Connexion de la touche Entrée
        self.ui.lineEditPasswordLogin.returnPressed.connect(
            self.check_credentials
        )  # Appuie sur "Entrée" pour se connecter

    def check_credentials(self):
        user = self.ui.lineEditUsernameLogin.text()
        password = self.ui.lineEditPasswordLogin.text()
        hashed_credentials = sha256((user + password).encode())
        if self.main_window.userRepo.login(
            user, hashed_credentials.hexdigest()
        ):
            parent = self.parentWidget()
            if isinstance(parent, QStackedWidget):
                parent.setCurrentIndex(1)
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials")
