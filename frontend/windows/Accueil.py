from PySide6.QtWidgets import QWidget, QStackedWidget, QMessageBox
from ui.ui_accueil import Ui_Accueil


class AccueilWindow(QWidget, Ui_Accueil):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.ui = Ui_Accueil()
        self.ui.setupUi(self)
        self.main_window = main_window  # Stockez la référence à MainWindow

        # Connexion des boutons
        self.ui.pushButtonDeconnexionAccueil.clicked.connect(self.logout)
        self.ui.pushButtonAttaquesAccueil.clicked.connect(self.goToAttaques)
        self.ui.pushButtonRapportsAccueil.clicked.connect(self.goToRapports)
        self.ui.pushButtonCartographieAccueil.clicked.connect(self.goToCartographie)

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

    def goToAttaques(self):
        self.main_window.mainStackedWidget.setCurrentIndex(self.main_window.mainStackedWidget.indexOf(self.main_window.attaquesPage))

    def goToRapports(self):
        self.main_window.mainStackedWidget.setCurrentIndex(self.main_window.mainStackedWidget.indexOf(self.main_window.rapportsPage))

    def goToCartographie(self):
        self.main_window.mainStackedWidget.setCurrentIndex(self.main_window.mainStackedWidget.indexOf(self.main_window.cartographiePage))
