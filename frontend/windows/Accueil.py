from PySide6.QtWidgets import QWidget, QStackedWidget, QMessageBox, QLineEdit
from ui.ui_accueil import Ui_Accueil


class AccueilWindow(QWidget, Ui_Accueil):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Accueil()
        self.ui.setupUi(self)
    
    #bouton déconnexion
        self.ui.pushButtonDeconnexionAccueil.clicked.connect(self.logout)

    #bouton attaques
        self.ui.pushButtonOnglet1Accueil.clicked.connect(self.goToAttacks)

    def logout(self):
        #Retourne à la page de login
        parent = self.parentWidget()
        if isinstance(parent, QStackedWidget):
            parent.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Erreur", "Impossible de revenir à la page de login")

    def goToAttacks(self):
        #Passe à la page Attaques
        parent = self.parentWidget()
        if isinstance(parent, QStackedWidget):
            parent.setCurrentIndex(2)  
        else:
            QMessageBox.warning(self, "Erreur", "Impossible d'aller à la page Attaques")


