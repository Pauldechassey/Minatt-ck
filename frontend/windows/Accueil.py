from PySide6.QtWidgets import QWidget, QStackedWidget, QMessageBox, QLineEdit
from ui.ui_accueil import Ui_Accueil


class AccueilWindow(QWidget, Ui_Accueil):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Accueil()
        self.ui.setupUi(self)
