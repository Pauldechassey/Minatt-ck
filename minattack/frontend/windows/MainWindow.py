from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QStackedWidget,
)

from minattack.frontend.repository.AttaquesRepo import AttaquesRepo
from minattack.frontend.repository.AuditRepo import AuditRepo
from minattack.frontend.repository.CartoRepo import CartoRepo
from minattack.frontend.repository.UserRepo import UserRepo
from minattack.frontend.repository.RapportRepo import RapportRepo
from minattack.frontend.ui.ui_main_window import Ui_MainWindow
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QLayout

from minattack.frontend.windows.Login import LoginWindow
from minattack.frontend.windows.Accueil import AccueilWindow
from minattack.frontend.windows.AuditsCreate import AuditsCreateWindow
from minattack.frontend.windows.AuditsSelect import AuditsSelectWindow
from minattack.frontend.windows.Attaques import AttaquesWindow
from minattack.frontend.windows.Rapports import RapportsWindow
from minattack.frontend.windows.Cartographie import CartographieWindow
from minattack.frontend.windows.Documentation import DocumentationWindow
from minattack.frontend.windows.Actualite import ActualiteWindow
from PySide6.QtGui import QIcon, QPixmap

import minattack.frontend.utils.settings as settings

from minattack.frontend.resources import resources_rc


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        settings.init_globals()
        settings.load_image()
        self.setupUi(self)

        self.userRepo = UserRepo()
        self.auditRepo = AuditRepo()
        self.cartoRepo = CartoRepo()
        self.attackRepo = AttaquesRepo()
        self.rapportRepo = RapportRepo()

        self.setStyleSheet("background-color: #121212; color: white;")
        self.setMinimumSize(1400, 900)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        layout = self.layout()
        if layout is not None:
            layout.setSizeConstraint(
                QLayout.SizeConstraint.SetDefaultConstraint
            )

        icon = QIcon(settings.LOGO_WINDOW)
        self.setWindowIcon(QPixmap(settings.LOGO_WINDOW))

        self.current_sd_id = None

        # Initialization des pages
        # Passez une référence à MainWindow
        self.loginPage = LoginWindow(self)
        self.accueilPage = AccueilWindow(self)
        self.auditsCreatePage = AuditsCreateWindow(self)
        self.auditsSelectPage = AuditsSelectWindow(self)
        self.cartographiePage = CartographieWindow(self)
        self.attaquesPage = AttaquesWindow(self)
        self.rapportsPage = RapportsWindow(self)
        self.documentationPage = DocumentationWindow(self)
        self.actualitePage = ActualiteWindow(self)

        # Ajout des pages au QStackedWidget
        self.mainStackedWidget.addWidget(self.loginPage)  # 0
        self.mainStackedWidget.addWidget(self.accueilPage)  # 1
        self.mainStackedWidget.addWidget(self.auditsCreatePage)  # 2
        self.mainStackedWidget.addWidget(self.auditsSelectPage)  # 3
        self.mainStackedWidget.addWidget(self.cartographiePage)  # 4
        self.mainStackedWidget.addWidget(self.attaquesPage)  # 5
        self.mainStackedWidget.addWidget(self.rapportsPage)  # 6
        self.mainStackedWidget.addWidget(self.documentationPage)  # 7
        self.mainStackedWidget.addWidget(self.actualitePage)  # 8

        # Définir la page initiale
        self.mainStackedWidget.setCurrentIndex(0)

    # Disconnect
    def logout(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Déconnexion")
        msg.setText("Voulez-vous vraiment vous déconnecter ?")
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel
        )
        msg.setIcon(QMessageBox.Icon.Question)
        result = msg.exec()
        if result == QMessageBox.StandardButton.Yes:
            if self.userRepo.logout():
                parent = self.parentWidget()
                self.loginPage.ui.lineEditUsernameLogin.clear()
                self.loginPage.ui.lineEditPasswordLogin.clear()
                self.mainStackedWidget.setCurrentIndex(0)
                if isinstance(parent, QStackedWidget):
                    self.mainStackedWidget.setCurrentIndex(0)
            else:
                QMessageBox.warning(self, "Error", "Deconnexion échoué")

    def goToAccueil(self):
        self.mainStackedWidget.setCurrentIndex(
            self.mainStackedWidget.indexOf(self.accueilPage)
        )

    def goToDocumentation(self):
        self.mainStackedWidget.setCurrentIndex(
            self.mainStackedWidget.indexOf(self.documentationPage)
        )

    def goToActualite(self):
        self.mainStackedWidget.setCurrentIndex(
            self.mainStackedWidget.indexOf(self.actualitePage)
        )

    def goToCartographie(self):
        self.mainStackedWidget.setCurrentIndex(
            self.mainStackedWidget.indexOf(self.cartographiePage)
        )

    def goToAttaque(self):
        self.mainStackedWidget.setCurrentIndex(
            self.mainStackedWidget.indexOf(self.attaquesPage)
        )

    def goToRapport(self):
        self.mainStackedWidget.setCurrentIndex(
            self.mainStackedWidget.indexOf(self.rapportsPage)
        )
