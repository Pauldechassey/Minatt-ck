from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from ui.ui_login import Ui_Login


class LoginWindow(QWidget, Ui_Login):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
