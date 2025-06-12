from typing import Any
from PySide6.QtWidgets import (
    QWidget,
    QMessageBox,
)
from minattack.frontend.ui.ui_attaques import Ui_Attaques
from PySide6.QtGui import QIcon, QPixmap

from minattack.frontend.utils import settings


class AttaquesWindow(QWidget, Ui_Attaques):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.ui = Ui_Attaques()
        self.ui.setupUi(self)
        self.main_window = main_window

        # Initializing decorative element
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
        self.ui.pushButtonActualiteAttaques.clicked.connect(
            self.main_window.goToActualite
        )
        self.ui.pushButtonDocumentationAttaques.clicked.connect(
            self.main_window.goToDocumentation
        )

        # Connecting page elements
        self.ui.pushButtonLancerAttaques.clicked.connect(self.manageAttaque)
        self.ui.pushButtonVisualiserAttaques.clicked.connect(
            self.main_window.cartographiePage.launchGraph
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

    def checkAuditStateAttaque(self) -> bool:
        # Vérification de l'état de l'audit
        if settings.SELECTED_AUDIT_STATE is None:
            QMessageBox.warning(
                self,
                "État inconnu",
                "L'état de l'audit n'est pas défini.",
            )
            return False
        elif (
            settings.SELECTED_AUDIT_STATE < 0
            or settings.SELECTED_AUDIT_STATE > 3
        ):
            QMessageBox.warning(
                self,
                "Attention",
                "Etat de l'audit invalide",
            )
            return False
        elif settings.SELECTED_AUDIT_STATE == 0:
            QMessageBox.warning(
                self,
                "Cartographie requise",
                "La cartographie doit être effectuée avant de lancer une attaque.",
            )
            return False
        elif settings.SELECTED_AUDIT_STATE > 1:
            QMessageBox.warning(
                self,
                "Attaque déjà effectuée",
                "Une attaque a déjà été lancée sur cet audit.",
            )
            return False
        else:
            return True

    def updateAuditStateAttaque(self):
        settings.SELECTED_AUDIT_STATE = settings.SELECTED_AUDIT_STATE + 1
        if self.main_window.auditRepo.updateAuditState(
            settings.SELECTED_AUDIT_ID, settings.SELECTED_AUDIT_STATE
        ):
            QMessageBox.information(
                self,
                "Succès",
                "Attaques lancées avec succès",
                QMessageBox.StandardButton.Cancel,
            )
            self.main_window.auditsSelectPage.populateComboBox()
            self.main_window.mainStackedWidget.setCurrentIndex(
                self.main_window.mainStackedWidget.indexOf(
                    self.main_window.rapportsPage
                )
            )
        else:
            QMessageBox.warning(
                self,
                "Attention",
                "Attaques réussies mais erreur lors de la mise à jour de l'état",
            )

    def checkSelectedAttaque(self) -> tuple[bool, Any]:
        selected_attacks = self.get_selected_attacks()
        if not selected_attacks:
            QMessageBox.warning(
                self,
                "Aucune sélection",
                "Veuillez sélectionner au moins une attaque.",
            )
            return False, None
        return True, selected_attacks

    def sendAttaque(self, selected_attacks):
        if self.ui.checkBoxClusterAttaques.isChecked():
            return self.main_window.attackRepo.send_attacks_cluster(
                settings.SELECTED_AUDIT_ID,
                selected_attacks,
            )
        else:
            return self.main_window.attackRepo.send_attacks(
                settings.SELECTED_AUDIT_ID,
                selected_attacks,
            )

    def manageAttaque(self):
        if (
            self.checkAuditStateAttaque()
            and (selected_attacks := self.checkSelectedAttaque())[0]
        ):
            results = self.sendAttaque(selected_attacks[1])
            if results:
                self.updateAuditStateAttaque()
                self.main_window.rapportsPage.manage_rapport()
            else:
                QMessageBox.critical(
                    self, "Erreur", "La cartographie a échoué"
                )
