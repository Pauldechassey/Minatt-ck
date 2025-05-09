from PySide6.QtWidgets import QWidget, QStackedWidget, QMessageBox, QLineEdit
from minattack.frontend.ui.ui_attaques import Ui_Attaques
from minattack.frontend.repository.AttaquesRepo import AttaquesRepo 


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

    def send_attacks(self, recursive=True):
        selected_attacks = self.get_selected_attacks()
        if not selected_attacks:
            QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner au moins une attaque.")
            return

        sd_initial_id = self.main_window.current_sd_id  

        repo = AttaquesRepo()
        if recursive:
            result = repo.send_attacks_recursive(sd_initial_id, selected_attacks)
        else:
            result = repo.send_attacks_single(sd_initial_id, selected_attacks)

        if result:
            QMessageBox.information(self, "Succès", result.get("message", "Attaque envoyée."))
        else:
            QMessageBox.critical(self, "Erreur", "Une erreur est survenue lors de l'envoi des attaques.")

    def get_selected_attacks(self) -> list[str]:
        selected = []
        if self.ui.checkBoxSQLI.isChecked():
            selected.append("sqli")
        if self.ui.checkBoxXSS.isChecked():
            selected.append("xss")
        if self.ui.checkBoxCSRF.isChecked():
            selected.append("csrf")
        if self.ui.checkBoxHEADERSCOOKIES.isChecked():
            selected.append("headers_cookies")
        return selected


