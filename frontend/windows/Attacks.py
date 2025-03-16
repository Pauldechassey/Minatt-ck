
from PySide6.QtWidgets import QWidget, QStackedWidget, QMessageBox, QLineEdit
from ui.ui_attacks import Ui_Attacks

class AttacksWindow(QWidget, Ui_Attacks):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.ui = Ui_Attacks()
        self.ui.setupUi(self)
        self.main_window = main_window

        # Connexion des boutons
        self.ui.pushButtonDeconnexionAttaques.clicked.connect(self.logout)
        self.ui.pushButtonOnglet2Attaques.clicked.connect(self.goToRapports)
        self.ui.pushButtonOnglet3Attaques.clicked.connect(self.goToCartographie)
        self.ui.pushButtonOngletAccueilAttaques.clicked.connect(self.goToAccueil)

    def logout(self):
        # Retourne à la page de login
        self.main_window.mainStackedWidget.setCurrentIndex(0)

    def goToCartographie(self):
        self.main_window.mainStackedWidget.setCurrentIndex(
            self.main_window.mainStackedWidget.indexOf(self.main_window.attacksPage)
        )

    def goToRapports(self):
        self.main_window.mainStackedWidget.setCurrentIndex(
            self.main_window.mainStackedWidget.indexOf(self.main_window.rapportsPage)
        )

    def goToAccueil(self):
        self.main_window.mainStackedWidget.setCurrentIndex(
            self.main_window.mainStackedWidget.indexOf(self.main_window.accueilPage)
        )
