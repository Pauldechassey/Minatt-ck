import sys
from PySide6.QtWidgets import QApplication, QWidget, QStackedWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QLineEdit
from PySide6.QtCore import Qt
from login import Ui_StackedWidget as Ui_Login
from accueil import Ui_Form as Ui_Accueil

class LoginApp(QStackedWidget):  # Hérite de QStackedWidget
    def __init__(self):
        super().__init__()  # Initialisation de QStackedWidget
        self.ui = Ui_Login()
        self.ui.setupUi(self)  # Initialise l'UI de la page de login
        self.login_page = QWidget()  # Crée la page de login
        self.addWidget(self.login_page)  # Ajoute la page de login au QStackedWidget

        # Connexion du bouton login
        self.ui.button_login.clicked.connect(self.handle_login)

        # Connexion de la touche Entrée
        self.ui.lineEdit_password.returnPressed.connect(self.handle_login)  # Appuie sur "Entrée" pour se connecter

        # Cacher le mot de passe
        self.ui.lineEdit_password.setEchoMode(QLineEdit.Password)  # Masquer le mot de passe

        # Centrer le formulaire de connexion
        self.center_login_form()

    def handle_login(self):
        username = self.ui.lineEdit_username.text()
        password = self.ui.lineEdit_password.text()

        # Vérification simple
        if username == "admin" and password == "password":
            self.setCurrentIndex(1)  # Aller à la page d'accueil (index 1)
        else:
            # Affichage d'un message d'erreur si les informations sont incorrectes
            QMessageBox.warning(self, "Erreur", "Nom d'utilisateur ou mot de passe incorrect")


class AccueilApp(QWidget):  # Page d'accueil (reste un QWidget)
    def __init__(self):
        super().__init__()
        self.ui = Ui_Accueil()  # Utilisation du généré Ui_Form pour la page d'accueil
        self.ui.setupUi(self)  # Configuration de l'UI de la page d'accueil

        # Ajout d'un simple texte pour vérifier si l'UI se charge correctement
        if hasattr(self.ui, "label"):  # Vérification qu'un label existe
            self.ui.label.setText("Bienvenue à la page d'accueil")  # Si label existe, change le texte

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Crée le conteneur principal (QStackedWidget)
    stacked_widget = QStackedWidget()

    # Crée les pages
    login_page = LoginApp()  # La page de login est maintenant un QStackedWidget
    accueil_page = AccueilApp()

    # Ajoute les pages au stacked widget
    stacked_widget.addWidget(login_page)
    stacked_widget.addWidget(accueil_page)

    # Affiche la page de login au départ
    stacked_widget.setCurrentIndex(0)
    stacked_widget.show()

    sys.exit(app.exec())




