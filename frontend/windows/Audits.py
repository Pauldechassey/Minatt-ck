from PySide6.QtWidgets import QMessageBox, QStackedWidget, QWidget
from ui.ui_audits import Ui_Audits
from repository.UserRepo import UserRepo
from repository.AuditRepo import AuditRepo


class AuditsWindow(QWidget, Ui_Audits):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)

        self.userRepo = UserRepo()
        self.auditRepo = AuditRepo()

        self.ui = Ui_Audits()
        self.ui.setupUi(self)
        self.main_window = main_window  # Stockez la référence à MainWindow

        # self.ui.pushButtonAttaquesAudits.setEnabled(False)
        # self.ui.pushButtonRapportsAudits.setEnabled(False)
        # self.ui.pushButtonCartographieAudits.setEnabled(False)

        # Connexion des boutons menu
        self.ui.pushButtonDeconnexionAudits.clicked.connect(self.logout)
        self.ui.pushButtonHomeAudits.clicked.connect(self.goToAccueil)
        self.ui.pushButtonAttaquesAudits.clicked.connect(self.goToAttaques)
        self.ui.pushButtonRapportsAudits.clicked.connect(self.goToRapports)
        self.ui.pushButtonCartographieAudits.clicked.connect(self.goToCartographie)

        # Connexion des boutons d'Audits
        self.ui.pushButtonAuditsAudits.clicked.connect(self.createAudit)

    # Creation d'un audit
    def createAudit(self):
        if self.auditRepo.createAudit(self.ui.lineEditUrlAudits.text()):
            QMessageBox.warning(self, "Error", "Création réussi")
        else:
            QMessageBox.warning(self, "Error", "Création ECHOUÉ")

    # Deconnexion
    def logout(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Déconnexion")
        msg.setText("Voulez-vous vraiment vous déconnecter ?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
        msg.setIcon(QMessageBox.Icon.Question)
        result = msg.exec()
        if result == QMessageBox.StandardButton.Yes:
            if self.userRepo.logout():
                parent = self.parentWidget()
                self.main_window.loginPage.ui.lineEditUsernameLogin.clear()
                self.main_window.loginPage.ui.lineEditPasswordLogin.clear()
                self.main_window.mainStackedWidget.setCurrentIndex(0)
                if isinstance(parent, QStackedWidget):
                    parent.setCurrentIndex(0)
            else:
                QMessageBox.warning(self, "Error", "Deconnexion échoué")

    # Changement de page
    def goToAccueil(self):
        self.main_window.mainStackedWidget.setCurrentIndex(self.main_window.mainStackedWidget.indexOf(self.main_window.accueilPage))

    def goToAttaques(self):
        self.main_window.mainStackedWidget.setCurrentIndex(self.main_window.mainStackedWidget.indexOf(self.main_window.attaquesPage))

    def goToRapports(self):
        self.main_window.mainStackedWidget.setCurrentIndex(self.main_window.mainStackedWidget.indexOf(self.main_window.rapportsPage))

    def goToCartographie(self):
        self.main_window.mainStackedWidget.setCurrentIndex(self.main_window.mainStackedWidget.indexOf(self.main_window.cartographiePage))
