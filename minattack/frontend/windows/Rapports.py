from PySide6.QtWidgets import (
    QWidget,
    QStackedWidget,
    QMessageBox,
    QLineEdit,
    QMainWindow,
)
from minattack.frontend.ui.ui_rapports import Ui_Rapports
from PySide6.QtGui import QIcon, QPixmap
from minattack.frontend.resources import resources_rc


class RapportsWindow(QWidget, Ui_Rapports):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.ui = Ui_Rapports()
        self.ui.setupUi(self)
        self.main_window = main_window  # Stockez la référence à MainWindow

        # Initializing decorative element
        self.ui.pushButtonDeconnexionRapports.setIcon(
            QIcon(":/images/deconnexion.png")
        )
        pixmap = QPixmap(":/images/logo.png")
        self.ui.labelLogo.setPixmap(pixmap)

        # Connecting menu buttons
        self.ui.pushButtonDeconnexionRapports.clicked.connect(
            self.main_window.logout
        )
        self.ui.pushButtonAccueilRapports.clicked.connect(
            self.main_window.goToAccueil
        )
        self.ui.pushButtonActualiteRapports.clicked.connect(
            self.main_window.goToActualite
        )
        self.ui.pushButtonDocumentationRapports.clicked.connect(
            self.main_window.goToDocumentation
        )
