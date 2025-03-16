from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget

from ui.ui_main_window import Ui_MainWindow

from windows.Accueil import AccueilWindow
from windows.Login import LoginWindow
from windows.Attacks import AttacksWindow
from windows.Rapports import RapportsWindow
from windows.Cartographie import CartographieWindow



class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Initialisation des pages
        self.loginPage = LoginWindow()
        self.accueilPage = AccueilWindow(self)  # Passez une référence à MainWindow
        self.attacksPage = AttacksWindow(self)
        self.rapportsPage = RapportsWindow(self)
        self.cartographiePage = CartographieWindow(self)

        # Ajout des pages au QStackedWidget
        self.mainStackedWidget.addWidget(self.loginPage)
        self.mainStackedWidget.addWidget(self.accueilPage)
        self.mainStackedWidget.addWidget(self.attacksPage)
        self.mainStackedWidget.addWidget(self.rapportsPage)
        self.mainStackedWidget.addWidget(self.cartographiePage)

        # Définir la page initiale
        self.mainStackedWidget.setCurrentIndex(0)

