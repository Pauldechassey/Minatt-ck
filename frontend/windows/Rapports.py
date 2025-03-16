
from PySide6.QtWidgets import QWidget, QStackedWidget, QMessageBox, QLineEdit
from ui.ui_rapports import Ui_Rapports

class RapportsWindow(QWidget, Ui_Rapports):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.ui = Ui_Rapports()
        self.ui.setupUi(self)
        self.main_window = main_window  # Stockez la référence à MainWindow

        # Connexion des boutons
        self.ui.pushButtonDeconnexionRapports.clicked.connect(self.logout)
        self.ui.pushButtonOnglet1Rapports.clicked.connect(self.goToAttacks)
        self.ui.pushButtonOnglet3Rapports.clicked.connect(self.goToCartographie)
        self.ui.pushButtonOngletAccueilRapports.clicked.connect(self.goToAccueil)

    def logout(self):
        # Retourne à la page de login
        self.main_window.mainStackedWidget.setCurrentIndex(0)

    def goToAttacks(self):
        self.main_window.mainStackedWidget.setCurrentIndex(
            self.main_window.mainStackedWidget.indexOf(self.main_window.attacksPage)
        )

    def goToCartographie(self):
        self.main_window.mainStackedWidget.setCurrentIndex(
            self.main_window.mainStackedWidget.indexOf(self.main_window.cartographiePage)
        )

    def goToAccueil(self):
        self.main_window.mainStackedWidget.setCurrentIndex(
            self.main_window.mainStackedWidget.indexOf(self.main_window.accueilPage)
        )