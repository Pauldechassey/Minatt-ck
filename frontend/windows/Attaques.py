from PySide6.QtWidgets import QWidget, QStackedWidget, QMessageBox, QLineEdit
from ui.ui_attaques import Ui_Attaques


class AttaquesWindow(QWidget, Ui_Attaques):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.ui = Ui_Attaques()
        self.ui.setupUi(self)
        self.main_window = main_window

        # Connexion des boutons
        self.ui.pushButtonDeconnexionAttaques.clicked.connect(self.logout)
        self.ui.pushButtonHomeAttaques.clicked.connect(self.goToAccueil)
        self.ui.pushButtonAuditsAttaques.clicked.connect(self.goToAudits)
        self.ui.pushButtonRapportsAttaques.clicked.connect(self.goToRapports)
        self.ui.pushButtonCartographieAttaques.clicked.connect(self.goToCartographie)

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

    def goToCartographie(self):
        self.main_window.mainStackedWidget.setCurrentIndex(self.main_window.mainStackedWidget.indexOf(self.main_window.cartographiePage))

    def goToRapports(self):
        self.main_window.mainStackedWidget.setCurrentIndex(self.main_window.mainStackedWidget.indexOf(self.main_window.rapportsPage))
