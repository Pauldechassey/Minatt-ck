
from PySide6.QtWidgets import QWidget, QStackedWidget, QMessageBox, QLineEdit
from ui.ui_attacks import Ui_Attacks

class AttacksWindow(QWidget, Ui_Attacks):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Attacks()
        self.ui.setupUi(self)

        # Bouton rechercher l'URL 
        #self.ui.pushButtonURLAttaques.clicked.connect(self.check_credentials)

        # Déconnexion
        self.ui.pushButtonDeconnexionAttaques.clicked.connect(self.logout)


    def logout(self):
        #Retourne à la page de login
        parent = self.parentWidget()
        if isinstance(parent, QStackedWidget):
            parent.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Erreur", "Impossible de revenir à la page de login")