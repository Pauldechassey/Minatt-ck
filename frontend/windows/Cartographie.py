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
        self.ui.pushButtonHomeCartographie.clicked.connect(self.goToAccueil)
        self.ui.pushButtonAuditsCartographie.clicked.connect(self.goToAudits)
        self.ui.pushButtonAttaquesCartographie.clicked.connect(self.goToAttaques)
        self.ui.pushButtonRapportsCartographie.clicked.connect(self.goToRapports)

    def logout(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Déconnexion")
        msg.setText("Voulez-vous vraiment vous déconnecter ?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
        msg.setIcon(QMessageBox.Icon.Question)

        result = msg.exec()

        if result == QMessageBox.StandardButton.Yes:
            self.main_window.loginPage.ui.lineEditUsernameLogin.clear()
            self.main_window.loginPage.ui.lineEditPasswordLogin.clear()
            self.main_window.mainStackedWidget.setCurrentIndex(0)

    def goToAccueil(self):
        self.main_window.mainStackedWidget.setCurrentIndex(self.main_window.mainStackedWidget.indexOf(self.main_window.accueilPage))

    def goToAudits(self):
        self.main_window.mainStackedWidget.setCurrentIndex(self.main_window.mainStackedWidget.indexOf(self.main_window.auditsPage))

    def goToAttaques(self):
        self.main_window.mainStackedWidget.setCurrentIndex(self.main_window.mainStackedWidget.indexOf(self.main_window.attaquesPage))

    def goToRapports(self):
        self.main_window.mainStackedWidget.setCurrentIndex(self.main_window.mainStackedWidget.indexOf(self.main_window.rapportsPage))
