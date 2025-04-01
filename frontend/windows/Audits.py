from PySide6.QtWidgets import QMessageBox, QWidget
from ui.ui_audits import Ui_Audits


class AuditsWindow(QWidget, Ui_Audits):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.ui = Ui_Audits()
        self.ui.setupUi(self)
        self.main_window = main_window  # Stockez la référence à MainWindow

        # Connexion des boutons
        self.ui.pushButtonDeconnexionAudits.clicked.connect(self.logout)
        self.ui.pushButtonHomeAudits.clicked.connect(self.goToAccueil)
        self.ui.pushButtonAttaquesAudits.clicked.connect(self.goToAttaques)
        self.ui.pushButtonRapportsAudits.clicked.connect(self.goToRapports)
        self.ui.pushButtonCartographieAudits.clicked.connect(self.goToCartographie)

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

    def goToAttaques(self):
        self.main_window.mainStackedWidget.setCurrentIndex(self.main_window.mainStackedWidget.indexOf(self.main_window.attaquesPage))

    def goToRapports(self):
        self.main_window.mainStackedWidget.setCurrentIndex(self.main_window.mainStackedWidget.indexOf(self.main_window.rapportsPage))

    def goToCartographie(self):
        self.main_window.mainStackedWidget.setCurrentIndex(self.main_window.mainStackedWidget.indexOf(self.main_window.cartographiePage))
