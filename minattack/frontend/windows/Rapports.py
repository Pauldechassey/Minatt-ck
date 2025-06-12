import base64
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWidgets import (
    QWidget,
    QMessageBox,
)
from PySide6.QtGui import QIcon, QPixmap
from minattack.frontend.ui.ui_rapports import Ui_Rapports
import os

from minattack.frontend.utils import settings


class RapportsWindow(QWidget, Ui_Rapports):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.ui = Ui_Rapports()
        self.ui.setupUi(self)
        self.main_window = main_window
        self.temp_pdf_path = None

        # Initializing decorative elements
        self.ui.pushButtonDeconnexionRapports.setIcon(
            QIcon(":/images/deconnexion.png")
        )
        pixmap = QPixmap(":/images/logo.png")
        self.ui.labelLogo.setPixmap(pixmap)
        self.setup_pdf_support()

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

        # Connecting page elements
        self.ui.pushButtonDownloadRapports.clicked.connect(
            self.download_rapport
        )
        self.ui.pushButtonVisualiserRapports.clicked.connect(
            self.main_window.cartographiePage.launchGraph
        )

    def setup_pdf_support(self):
        settings = self.ui.qWebEngineViewPdfRapports.settings()

        # Paramètres essentiels pour les PDF
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.PdfViewerEnabled, True
        )
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.PluginsEnabled, True
        )
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.JavascriptEnabled, True
        )

        # Paramètres de sécurité
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls,
            True,
        )
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True
        )

        # Paramètres d'affichage
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.AutoLoadImages, True
        )
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.ErrorPageEnabled, True
        )

    print("Configuration PDF appliquée")

    def download_rapport(self):
        if (
            file_path := self.main_window.rapportRepo.get_data_rapport(
                settings.SELECTED_AUDIT_ID
            )
        )[0]:
            QMessageBox.information(
                self,
                "Succès",
                f"Rapport enregistré  {file_path}",
                QMessageBox.StandardButton.Cancel,
            )
        else:
            QMessageBox.warning(
                self, "Erreur", "Échec du téléchargement du rapport"
            )

    def manage_rapport(self):
        if (
            results := self.main_window.rapportRepo.download_rapport(
                settings.SELECTED_AUDIT_ID
            )
        )[0]:
            if os.path.exists(results[1]):
                settings.SELECTED_RAPPORT_PATH = results[1]
                self.ui.qWebEngineViewPdfRapports.setHtml(
                    self.load_pdf_as_html()
                )
            else:
                QMessageBox.warning(self, "Attention", "PDF non trouve")
        else:
            QMessageBox.critical(
                self, "Erreur", "Echec du téléchargement du rapport"
            )

    def load_pdf_as_html(self) -> str:
        with open(settings.SELECTED_RAPPORT_PATH, "rb") as f:
            pdf_data = f.read()
        pdf_base64 = base64.b64encode(pdf_data).decode("utf-8")
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <style>
            body {{ margin: 0; padding: 0; height: 100vh; }}
            object {{ width: 100%; height: 100%; }}
        </style>
        </head>
        <body>
            <object data="data:application/pdf;base64,{pdf_base64}"
                    type="application/pdf"
                    width="100%"
                    height="100%">
            </object>
        </body>
        </html>
        """
        return html_content
