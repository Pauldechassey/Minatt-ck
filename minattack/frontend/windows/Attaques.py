from PySide6.QtWidgets import (
    QWidget,
    QMessageBox,
)
from minattack.frontend.ui.ui_attaques import Ui_Attaques
from minattack.frontend.repository.AttaquesRepo import AttaquesRepo
from PySide6.QtGui import QIcon, QPixmap
from minattack.frontend.utils import settings


class AttaquesWindow(QWidget, Ui_Attaques):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.ui = Ui_Attaques()
        self.ui.setupUi(self)
        self.main_window = main_window

        # Initialising decorative element
        self.ui.pushButtonDeconnexionAttaques.setIcon(
            QIcon(":/images/deconnexion.png")
        )
        pixmap = QPixmap(":/images/logo.png")
        self.ui.labelLogo.setPixmap(pixmap)

        # Connecting menu buttons
        self.ui.pushButtonDeconnexionAttaques.clicked.connect(
            self.main_window.logout
        )
        self.ui.pushButtonAccueilAttaques.clicked.connect(
            self.main_window.goToAccueil
        )
        # self.ui.pushButtonActualiteAuditsCreate.clicked.connect(
        #     self.goToAttaques
        # )
        # self.ui.pushButtonDocumentationAuditsCreate.clicked.connect(
        #     self.goToRapports
        # )

        # Connecting page elements
        self.ui.pushButtonLancerAttaques.clicked.connect(self.send_attacks)

    def goToAccueil(self):
        self.main_window.mainStackedWidget.setCurrentIndex(
            self.main_window.mainStackedWidget.indexOf(
                self.main_window.accueilPage
            )
        )

    def send_attacks(self, recursive=True):

        # Vérification de l'état de l'audit
        if settings.SELECTED_AUDIT_STATE is None:
            QMessageBox.warning(
                self,
                "État inconnu",
                "L'état de l'audit n'est pas défini.",
            )
            return
        elif settings.SELECTED_AUDIT_STATE == 0:
            QMessageBox.warning(
                self,
                "Cartographie requise",
                "La cartographie doit être effectuée avant de lancer une attaque.",
            )
            return
        elif settings.SELECTED_AUDIT_STATE == 2:
            QMessageBox.warning(
                self,
                "Attaque déjà effectuée",
                "Une attaque a déjà été lancée sur cet audit.",
            )
            return

        selected_attacks = self.get_selected_attacks()
        if not selected_attacks:
            QMessageBox.warning(
                self,
                "Aucune sélection",
                "Veuillez sélectionner au moins une attaque.",
            )
            return

        sd_initial_id = settings.SELECTED_AUDIT_ID

        repo = AttaquesRepo()
        if recursive:
            result = repo.send_attacks_recursive(
                sd_initial_id, selected_attacks
            )
        else:
            result = repo.send_attacks_single(
                sd_initial_id, selected_attacks, settings.SELECTED_AUDIT_STATE
            )

        if result:
            if self.main_window.auditRepo.update_audit_state(
                settings.SELECTED_AUDIT_ID, 2
            ):
                settings.SELECTED_AUDIT_STATE = 2
                self.main_window.auditsPage.populateComboBox()
                QMessageBox.information(
                    self,
                    "Succès",
                    "Attaques lancées avec succès",
                    QMessageBox.StandardButton.Cancel,
                )
            else:
                QMessageBox.warning(
                    self,
                    "Attention",
                    "Attaques réussies mais erreur lors de la mise à jour de l'état",
                )

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
