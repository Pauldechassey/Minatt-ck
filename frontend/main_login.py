import sys
from PySide6.QtWidgets import QApplication, QStackedWidget, QMessageBox
from login import Ui_StackedWidget  # Interface générée avec pyside6-uic

class LoginApp(QStackedWidget):
    def __init__(self):
        super().__init__()  # Appelle le constructeur de QStackedWidget
        self.ui = Ui_StackedWidget()  # Crée une instance de Ui_StackedWidget
        self.ui.setupUi(self)  # Configure l'interface utilisateur

        # Connecter le bouton login
        self.ui.button_login.clicked.connect(self.handle_login)

    def handle_login(self):
        username = self.ui.lineEdit_username.text()
        password = self.ui.lineEdit_password.text()

        # Vérification simple (à adapter avec ta logique réelle)
        if username == "admin" and password == "password":
            QMessageBox.information(self, "Succès", "Connexion réussie ! 🎉")
        else:
            QMessageBox.warning(self, "Erreur", "Nom d'utilisateur ou mot de passe incorrect")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginApp()  # Crée une instance de LoginApp (QStackedWidget)
    window.show()  # Affiche l'interface graphique
    sys.exit(app.exec())  # Lance la boucle d'événements

