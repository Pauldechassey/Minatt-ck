from PySide6.QtWidgets import (
    QWidget,
    QStackedWidget,
    QMessageBox,
    QLineEdit,
    QMainWindow,
)
from minattack.frontend.ui.ui_actualite import Ui_Actualite
from PySide6.QtGui import QIcon, QPixmap
from minattack.frontend.resources import resources_rc


class ActualiteWindow(QWidget, Ui_Actualite):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.ui = Ui_Actualite()
        self.ui.setupUi(self)
        self.main_window = main_window  # Stockez la référence à MainWindow

        # Initialising decorative element
        self.ui.pushButtonDeconnexionActualite.setIcon(
            QIcon(":/images/deconnexion.png")
        )
        pixmap = QPixmap(":/images/logo.png")
        self.ui.labelLogo_2.setPixmap(pixmap)

        # Connecting menu buttons
        self.ui.pushButtonDeconnexionActualite.clicked.connect(
            self.main_window.logout
        )
        self.ui.pushButtonAccueilActualite.clicked.connect(
            self.main_window.goToAccueil
        )
        self.ui.pushButtonDocumentationActualite.clicked.connect(
            self.main_window.goToDocumentation
        )