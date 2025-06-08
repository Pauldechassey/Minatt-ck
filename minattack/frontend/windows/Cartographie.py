from PySide6.QtWidgets import QWidget, QMessageBox
from minattack.frontend.ui.ui_cartographie import Ui_Cartographie

from PySide6.QtGui import QIcon, QPixmap

import minattack.frontend.utils.settings as settings


class CartographieWindow(QWidget, Ui_Cartographie):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.ui = Ui_Cartographie()
        self.ui.setupUi(self)
        self.main_window = main_window  # Stockez la référence à MainWindow

        # Initialising decorative element
        self.ui.pushButtonDeconnexionCartographie.setIcon(
            QIcon(":/images/deconnexion.png")
        )
        pixmap = QPixmap(":/images/logo.png")
        self.ui.labelLogo.setPixmap(pixmap)

        # Connecting menu buttons
        self.ui.pushButtonDeconnexionCartographie.clicked.connect(
            self.main_window.logout
        )
        self.ui.pushButtonAccueilCartographie.clicked.connect(
            self.main_window.goToAccueil
        )
        # self.ui.pushButtonActualiteAuditsCreate.clicked.connect(
        #     self.goToAttaques
        # )
        # self.ui.pushButtonDocumentationAuditsCreate.clicked.connect(
        #     self.goToRapports
        # )

        # Connecting page elemets
        self.ui.pushButtonLancerCartographie.clicked.connect(self.manageCarto)
        self.ui.checkBoxFuzzingCartographie.clicked.connect(
            self.checkFuzzSelect
        )

    def checkFuzzSelect(self):
        if self.ui.checkBoxFuzzingCartographie.isChecked():
            self.ui.lineEditWordlistPathCartographie.setEnabled(True)
        else:
            self.ui.lineEditWordlistPathCartographie.clear()
            self.ui.lineEditWordlistPathCartographie.setEnabled(False)

    def checkAuditStateCartographie(self) -> bool:
        if settings.SELECTED_AUDIT_STATE > 0:
            QMessageBox.warning(
                self,
                "Attention",
                "La cartographie a déjà été effectuée pour cet audit",
            )
            return False
        elif settings.SELECTED_AUDIT_STATE < 0:
            QMessageBox.warning(
                self,
                "Attention",
                "Etat de l'audit invalide",
            )
            return False
        else:
            return True

    def updateAuditStateCartographie(self):
        settings.SELECTED_AUDIT_STATE = settings.SELECTED_AUDIT_STATE + 1
        if self.main_window.auditRepo.updateAuditState(
            settings.SELECTED_AUDIT_ID, settings.SELECTED_AUDIT_STATE
        ):
            QMessageBox.information(
                self,
                "Succès",
                "Cartographie réalisée avec succès",
                QMessageBox.StandardButton.Cancel,
            )
            self.main_window.auditsSelectPage.populateComboBox()
            self.main_window.mainStackedWidget.setCurrentIndex(
                self.main_window.mainStackedWidget.indexOf(
                    self.main_window.attaquesPage
                )
            )
        else:
            QMessageBox.warning(
                self,
                "Attention",
                "Cartographie réussie mais erreur lors de la mise à jour de l'état",
            )

    def launchCarto(self, fuzzing: bool, wordlist_path: str):
        if self.main_window.cartoRepo.runCarto(
            settings.SELECTED_AUDIT_ID, fuzzing, wordlist_path
        ):
            self.updateAuditStateCartographie()
        else:
            settings.SELECTED_AUDIT_STATE = settings.SELECTED_AUDIT_STATE - 1
            QMessageBox.critical(self, "Erreur", "La cartographie a échoué")

    def manageCarto(self):
        check = self.checkAuditStateCartographie()
        fuzzing = self.ui.checkBoxFuzzingCartographie.isChecked()
        wordlist_path = self.ui.lineEditWordlistPathCartographie.text()
        if check and fuzzing is False:
            self.launchCarto(fuzzing, "")
        elif check and fuzzing is True:
            self.launchCarto(fuzzing, wordlist_path)
