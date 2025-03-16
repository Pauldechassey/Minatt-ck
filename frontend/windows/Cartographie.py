from PySide6.QtWidgets import QWidget, QStackedWidget, QMessageBox
from ui.ui_cartographie import Ui_Cartographie

class CartographieWindow(QWidget, Ui_Cartographie):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.ui = Ui_Cartographie()
        self.ui.setupUi(self)
        self.main_window = main_window  # Stockez la référence à MainWindow

        # Connexion des boutons
        self.ui.pushButtonDeconnexionCartographie.clicked.connect(self.logout)
        self.ui.pushButtonOnglet1Cartographie.clicked.connect(self.goToAttacks)
        self.ui.pushButtonOnglet2Cartographie.clicked.connect(self.goToRapports)
        self.ui.pushButtonOngletAccueilCartographie.clicked.connect(self.goToAccueil)

    def logout(self):
        # Retourne à la page de login
        self.main_window.mainStackedWidget.setCurrentIndex(0)

    def goToAttacks(self):
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
