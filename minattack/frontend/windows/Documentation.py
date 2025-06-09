from PySide6.QtWidgets import (
    QWidget,
)
from minattack.frontend.ui.ui_documentation import Ui_Documentation
from PySide6.QtGui import QIcon, QPixmap
from minattack.frontend.resources import resources_rc


class DocumentationWindow(QWidget, Ui_Documentation):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.ui = Ui_Documentation()
        self.ui.setupUi(self)
        self.main_window = main_window  # Stockez la référence à MainWindow

        # Initializing decorative element
        self.ui.pushButtonDeconnexionDocumentation.setIcon(
            QIcon(":/images/deconnexion.png")
        )
        pixmap = QPixmap(":/images/logo.png")
        self.ui.labelLogo.setPixmap(pixmap)

        # Connecting menu buttons
        self.ui.pushButtonDeconnexionDocumentation.clicked.connect(
            self.main_window.logout
        )
        self.ui.pushButtonAccueilDocumentation.clicked.connect(
            self.main_window.goToAccueil
        )
        self.ui.pushButtonActualiteDocumentation.clicked.connect(
            self.main_window.goToActualite
        )
