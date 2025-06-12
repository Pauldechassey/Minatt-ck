from PySide6.QtWidgets import QWidget
from minattack.frontend.ui.ui_audits_select import Ui_AuditsSelect
from PySide6.QtGui import QIcon, QPixmap

import minattack.frontend.utils.settings as settings


class AuditsSelectWindow(QWidget, Ui_AuditsSelect):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.ui = Ui_AuditsSelect()
        self.ui.setupUi(self)
        self.main_window = main_window

        # Initializing decorative element
        self.ui.pushButtonDeconnexionAuditsSelect.setIcon(
            QIcon(":/images/deconnexion.png")
        )
        pixmap = QPixmap(":/images/logo.png")
        self.ui.labelLogo.setPixmap(pixmap)

        # Fill the combobox on loading of the page
        self.populateComboBox()

        # Connecting menu buttons
        self.ui.pushButtonDeconnexionAuditsSelect.clicked.connect(
            self.main_window.logout
        )
        self.ui.pushButtonAccueilAuditsSelect.clicked.connect(
            self.main_window.goToAccueil
        )
        self.ui.pushButtonActualiteAuditsSelect.clicked.connect(
            self.main_window.goToActualite
        )
        self.ui.pushButtonDocumentationAuditsSelect.clicked.connect(
            self.main_window.goToDocumentation
        )

        # Connecting page elemets
        self.ui.pushButtonSelectionUrlAuditsSelect.clicked.connect(
            self.selectAudit
        )

    def populateComboBox(self):
        self.ui.comboBoxSelectionUrlAuditsSelect.clear()
        success, data = self.main_window.auditRepo.getAuditsDomaines()
        if success:
            for element in data:
                self.ui.comboBoxSelectionUrlAuditsSelect.addItem(
                    f"{element['id_audit']} : {element['date']} ~ {element['url_domaine']} | {element['etat']}"
                )

    def updateAuditStateSelect(self, id: int, state: int):
        settings.SELECTED_AUDIT_ID = id
        settings.SELECTED_AUDIT_STATE = state

    def selectAudit(self):
        choice = self.ui.comboBoxSelectionUrlAuditsSelect.currentText()
        self.updateAuditStateSelect(
            int(choice.split(" : ")[0]), int(choice.split(" | ")[1])
        )
        if settings.SELECTED_AUDIT_STATE == 0:
            self.main_window.mainStackedWidget.setCurrentIndex(
                self.main_window.mainStackedWidget.indexOf(
                    self.main_window.cartographiePage
                )
            )
        elif settings.SELECTED_AUDIT_STATE == 1:
            self.main_window.mainStackedWidget.setCurrentIndex(
                self.main_window.mainStackedWidget.indexOf(
                    self.main_window.attaquesPage
                )
            )
        elif settings.SELECTED_AUDIT_STATE in [2, 3]:
            self.main_window.mainStackedWidget.setCurrentIndex(
                self.main_window.mainStackedWidget.indexOf(
                    self.main_window.rapportsPage
                )
            )
            self.main_window.rapportsPage.manage_rapport()
