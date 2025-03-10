from PySide6.QtWidgets import QWidget, QStackedWidget, QMessageBox, QLineEdit
from ui.ui_login import Ui_Login


class LoginWindow(QWidget, Ui_Login):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Login()
        self.ui.setupUi(self)

        # Connexion du bouton login
        self.ui.buttonLogin.clicked.connect(self.check_credentials)

        # Connexion de la touche Entrée
        self.ui.lineEditPasswordLogin.returnPressed.connect(self.check_credentials)  # Appuie sur "Entrée" pour se connecter

    def check_credentials(self):
        if self.ui.lineEditUsernameLogin.text() == "admin" and self.ui.lineEditPasswordLogin.text() == "admin":
            parent = self.parentWidget()
            if isinstance(parent, QStackedWidget):
                parent.setCurrentIndex(1)
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials")
