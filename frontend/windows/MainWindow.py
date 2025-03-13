from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget

from ui.ui_main_window import Ui_MainWindow

from windows.Accueil import AccueilWindow
from windows.Login import LoginWindow
from windows.Attacks import AttacksWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.loginPage = LoginWindow()
        self.accueilPage = AccueilWindow()
        self.attacksPage = AttacksWindow()
        self.mainStackedWidget.addWidget(self.loginPage)
        self.mainStackedWidget.addWidget(self.accueilPage)
        self.mainStackedWidget.addWidget(self.attacksPage)
        self.mainStackedWidget.setCurrentIndex(0)
