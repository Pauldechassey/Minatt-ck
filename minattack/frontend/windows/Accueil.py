from PySide6.QtWidgets import QWidget
from minattack.frontend.ui.ui_accueil import Ui_Accueil
from PySide6.QtGui import QIcon, QPixmap


class AccueilWindow(QWidget, Ui_Accueil):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.ui = Ui_Accueil()
        self.ui.setupUi(self)
        self.main_window = main_window

        # Initializing decorative elements
        self.ui.pushButtonDeconnexionAccueil.setIcon(
            QIcon(":/images/deconnexion.png")
        )
        pixmap = QPixmap(":/images/logo.png")
        self.ui.labelLogo.setPixmap(pixmap)

        # Connecting menu buttons
        self.ui.pushButtonDeconnexionAccueil.clicked.connect(
            self.main_window.logout
        )

        # Connecting page buttons
        self.ui.pushButtonCreateAudit.clicked.connect(self.goToAuditsCreate)
        self.ui.pushButtonSelectAudit.clicked.connect(self.goToAuditsSelect)
        
        self.ui.pushButtonDocumentationAccueil.setEnabled(True)
        self.ui.pushButtonActualiteAccueil.setEnabled(True)
        self.ui.pushButtonDocumentationAccueil.clicked.connect(self.goToDocumentation)
        self.ui.pushButtonActualiteAccueil.clicked.connect(self.goToActualite)

    def goToAuditsCreate(self):
        self.main_window.mainStackedWidget.setCurrentIndex(
            self.main_window.mainStackedWidget.indexOf(
                self.main_window.auditsCreatePage
            )
        )

    def goToAuditsSelect(self):
        self.main_window.mainStackedWidget.setCurrentIndex(
            self.main_window.mainStackedWidget.indexOf(
                self.main_window.auditsSelectPage
            )
        )
        
    def goToDocumentation(self):
        self.main_window.mainStackedWidget.setCurrentIndex(
            self.main_window.mainStackedWidget.indexOf(
                self.main_window.documentationPage
            )
        )
        
    def goToActualite(self):
        self.main_window.mainStackedWidget.setCurrentIndex(
            self.main_window.mainStackedWidget.indexOf(
                self.main_window.actualitePage
            )
        )
