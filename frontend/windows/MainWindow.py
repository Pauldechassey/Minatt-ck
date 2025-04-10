from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget

from ui.ui_main_window import Ui_MainWindow
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QLayout

from windows.Login import LoginWindow
from windows.Accueil import AccueilWindow
from windows.Audits import AuditsWindow
from windows.Attaques import AttaquesWindow
from windows.Rapports import RapportsWindow
from windows.Cartographie import CartographieWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setStyleSheet("background-color: #121212; color: white;")
        self.setMinimumSize(800, 600)  # Taille minimale pour éviter une fenêtre trop petite
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout = self.layout()
        if layout is not None:
            layout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)

        # Initialisation des pages
        self.loginPage = LoginWindow()
        self.accueilPage = AccueilWindow(self)  # Passez une référence à MainWindow
        self.auditsPage = AuditsWindow(self)
        self.attaquesPage = AttaquesWindow(self)
        self.rapportsPage = RapportsWindow(self)
        self.cartographiePage = CartographieWindow(self)

        # Ajout des pages au QStackedWidget
        self.mainStackedWidget.addWidget(self.loginPage)
        self.mainStackedWidget.addWidget(self.accueilPage)
        self.mainStackedWidget.addWidget(self.auditsPage)
        self.mainStackedWidget.addWidget(self.attaquesPage)
        self.mainStackedWidget.addWidget(self.rapportsPage)
        self.mainStackedWidget.addWidget(self.cartographiePage)

        # Définir la page initiale
        self.mainStackedWidget.setCurrentIndex(0)
