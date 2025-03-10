from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from ui.ui_main_window import Ui_MainWindow
from windows.Login import LoginWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.loginPage = LoginWindow()
        self.mainStackedWidget.addWidget(self.loginPage)
        self.mainStackedWidget.setCurrentIndex(1)
