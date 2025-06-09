from PySide6.QtWidgets import QMessageBox, QWidget
from minattack.frontend.ui.ui_audits_create import Ui_AuditsCreate
from PySide6.QtGui import QIcon, QPixmap

import minattack.frontend.utils.settings as settings


class AuditsCreateWindow(QWidget, Ui_AuditsCreate):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.ui = Ui_AuditsCreate()
        self.ui.setupUi(self)
        self.main_window = main_window

        # Initializing decorative element
        self.ui.pushButtonDeconnexionAuditsCreate.setIcon(
            QIcon(":/images/deconnexion.png")
        )
        pixmap = QPixmap(":/images/logo.png")
        self.ui.labelLogo.setPixmap(pixmap)

        # Connecting menu buttons
        self.ui.pushButtonDeconnexionAuditsCreate.clicked.connect(
            self.main_window.logout
        )
        self.ui.pushButtonAccueilAuditsCreate.clicked.connect(
            self.main_window.goToAccueil
        )
        self.ui.pushButtonActualiteAuditsCreate.clicked.connect(
            self.main_window.goToActualite
        )
        self.ui.pushButtonDocumentationAuditsCreate.clicked.connect(
            self.main_window.goToDocumentation
        )

        # Connecting page elements
        self.ui.pushButtonCreerAuditsCreate.clicked.connect(self.createAudit)

        # Disabling url validity warning
        self.ui.labelWarningUrlAuditsCreate.setEnabled(False)

    def updateAuditStateCreate(self, id: int):
        settings.SELECTED_AUDIT_ID = id
        settings.SELECTED_AUDIT_STATE = 0

    # Creation d'un audit
    def createAudit(self):
        url = self.ui.lineEditUrlAuditsCreate.text()
        if url == "":
            self.ui.labelWarningUrlAuditsCreate.setEnabled(True)
            self.ui.labelWarningUrlAuditsCreate.setText(
                "L'url ne peut pas être vide"
            )
            self.ui.labelWarningUrlAuditsCreate.setStyleSheet(
                "QLabel {color: red;}"
            )
        elif (
            url != ""
            and (result := self.main_window.auditRepo.createAudit(url))[0]
        ):
            self.ui.labelWarningUrlAuditsCreate.setEnabled(True)
            self.ui.labelWarningUrlAuditsCreate.setText(
                "Création de l'audit réussi"
            )
            self.ui.labelWarningUrlAuditsCreate.setStyleSheet(
                "QLabel {color: green;}"
            )
            self.updateAuditStateCreate(result[1])
            self.main_window.auditsSelectPage.populateComboBox()
            self.main_window.mainStackedWidget.setCurrentIndex(
                self.main_window.mainStackedWidget.indexOf(
                    self.main_window.cartographiePage
                )
            )
        else:
            QMessageBox.critical(self, "Erreur", "Création d'audit ECHOUÉ")
