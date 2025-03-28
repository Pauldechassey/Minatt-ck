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
        self.ui.pushButtonAttaquesRapports.clicked.connect(self.goToAttacks)
        self.ui.pushButtonCartographieRapports.clicked.connect(self.goToCartographie)
        self.ui.pushButtonHomeRapports.clicked.connect(self.goToAccueil)

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

    def goToAttacks(self):
        self.main_window.mainStackedWidget.setCurrentIndex(self.main_window.mainStackedWidget.indexOf(self.main_window.attacksPage))

    def goToCartographie(self):
        self.main_window.mainStackedWidget.setCurrentIndex(self.main_window.mainStackedWidget.indexOf(self.main_window.cartographiePage))

    def goToAccueil(self):
        self.main_window.mainStackedWidget.setCurrentIndex(self.main_window.mainStackedWidget.indexOf(self.main_window.accueilPage))
